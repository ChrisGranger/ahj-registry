<template>
  <div id="mapdiv">
  </div>
</template>

<script>
import L from "leaflet";
import "leaflet-draw";
import constants from "../../constants.js";

export default {
  name: "Map",
  props: ['filterToggled'],
  data() {
    return {
      leafletMap: null,
      polygonLayer: null,
      currSearchMarker: null,
      markerLayerGroup: null,
      searchPolygonFeatureGroup: null,
      controlLayer: null,
      previousPolygonAPIPage: "", // empty string so that it is different on the first page where previous === null
    };
  },
  methods: {
    /*
     * Initialize the leaflet map and set it as the store's leaflet map
     */
    setupLeafletMap() {

      // initialize the map
      this.leafletMap = L.map("mapdiv").setView(
          constants.MAP_INIT_CENTER,
          constants.MAP_INIT_ZOOM
      );

      // add the tiles to the map
      L.tileLayer(constants.MAP_TILE_API_URL, {
        attribution: constants.MAP_TILE_API_ATTR
      }).addTo(this.leafletMap);

      // add the zoom button to the bottom right of the map
      this.leafletMap.zoomControl.setPosition('bottomright');
      this.markerLayerGroup = L.layerGroup().addTo(this.leafletMap);
      this.addDrawingTools();
    },
    addDrawingTools(){
      this.searchPolygonFeatureGroup = new L.FeatureGroup();
      this.leafletMap.addLayer(this.searchPolygonFeatureGroup);

      // add the polygon/region drawing tool
      this.controlLayer =  new L.Control.Draw({
        draw: {
          polyline: false,
          rectangle: false,
          circle: false,
          circlemarker: false
        },
        edit: {
          featureGroup: this.searchPolygonFeatureGroup
        }
      }).addTo(this.leafletMap);
      this.registerLeafletDrawHandlers();
    },
    /**
     * Helper for adding listeners to polygon/region drawing tool functions
     */
    registerLeafletDrawHandlers() {
      let that = this;

      // set a searched polygon/region when its created
      this.leafletMap.on('draw:created', function (e) {
        let layer = e.layer;
        that.searchPolygonFeatureGroup.addLayer(layer);
        that.$store.commit('setSearchGeoJSON', that.searchPolygonFeatureGroup.toGeoJSON());
      });

      // set a searched polygon/region when its created
      this.leafletMap.on('draw:editstop', function() {
        that.$store.commit('setSearchGeoJSON', that.searchPolygonFeatureGroup.toGeoJSON());
      });

      // reset the searched polygon/region when its modified
      this.leafletMap.on('draw:deletestop', function() {
        let geojson = that.searchPolygonFeatureGroup.toGeoJSON();
        if (geojson.features.length === 0) {
          geojson = null;
        }
        that.$store.commit('setSearchGeoJSON', geojson);
      });
    },
    // Replace map's existing polygons and markers with ones from the new search
    updateMap(ahjlist) {
      ahjlist = ahjlist.filter(ahj => ahj.Polygon !== null);
      this.markerLayerGroup.clearLayers();
      this.addPolygonLayer(ahjlist);
      this.updateMapMarkers(ahjlist);
    },
    /**
     * Add polygons of the given ahjs to the map.
     * Expects all AHJs in the passed-in list have GeoJSON polygons.
     */
    addPolygonLayer(ahjlist) {
      let polygons = ahjlist.map(ahj => ahj.Polygon);
      if (polygons.length === 0) {
        return;
      }
      this.polygonLayer = L.geoJSON(polygons, {
        style: constants.MAP_PLYGN_SYTLE
      });
      this.polygonLayer.addTo(this.leafletMap);
      let initialPolygonSelected = polygons[0];
      this.selectPolygon(initialPolygonSelected.properties.AHJID);
    },
    /**
     * Select a polygon existing on the map
     */
    selectPolygon(newAHJID) {
      let map = this.leafletMap;
      map.eachLayer(function(layer) {
        if (layer.feature) {
          if (layer.feature.properties.AHJID === newAHJID) {
            map.fitBounds(layer.getBounds());
            layer.setStyle(constants.MAP_PLYGN_SLCTD_SYTLE());
          } else {
            layer.setStyle(constants.MAP_PLYGN_SYTLE());
          }
        }
      });
    },
    /**
     * Set the map markers for the ahj offices and the searched address, if any.
     * Expects all AHJs in the passed-in list have GeoJSON polygons.
     */
    updateMapMarkers(ahjlist) {
      let location = this.$store.state.apiData.results.Location;

      // set the searched address marker
      if (location["Latitude"]["Value"] !== null) {
        let searchMarker = L.AwesomeMarkers.icon({
          icon: "circle",
          prefix: "fa",
          markerColor: "cadetblue"
        });
        let searchedLocation = [
          location["Latitude"]["Value"],
          location["Longitude"]["Value"]
        ];
        this.currSearchMarker = L.marker(searchedLocation, {
          icon: searchMarker
        })
          .bindTooltip("Searched Address")
          .addTo(this.leafletMap);
      }
      for (let ahj of ahjlist) {
        let polygon = ahj.Polygon;
        let ahjMarker = L.AwesomeMarkers.icon({
          icon: "building",
          prefix: "fa",
          markerColor: this.selectMarkerColor(polygon)
        });

        // set the ahj office markers
        let ahjOfficeLocation = null;
        let ahjOfficeMarkerTooltipMsg = `<b>${ahj.AHJName.Value}</b><br><b>Address</b>: `;
        if (ahj.Address && ahj.Address.Location && ahj.Address.Location["Latitude"]["Value"] && ahj.Address.Location["Longitude"]["Value"]) {
          ahjOfficeLocation = [
            ahj.Address.Location["Latitude"]["Value"],
            ahj.Address.Location["Longitude"]["Value"]
          ];
          ahjOfficeMarkerTooltipMsg += "<br>" + this.getAHJOfficeAddress(ahj);
        } else { // unknown ahj office location
          ahjOfficeLocation = [
            polygon.properties["InternalPLatitude"],
            polygon.properties["InternalPLongitude"]
          ];
          ahjOfficeMarkerTooltipMsg += "The AHJ Registry does not have an Address for this AHJ";
        }
        let marker = L.marker(ahjOfficeLocation, {
          icon: ahjMarker,
          riseOnHover: true
        })
          .bindTooltip(ahjOfficeMarkerTooltipMsg)
          .addTo(this.markerLayerGroup);
        let that = this;
        marker.on("click", function() {
          that.$store.commit("setSelectedAHJ", ahj);
        });
      }
    },
    /**
     * Set the makrer color of the ahj office based on GEOID
     */
    selectMarkerColor(polygon) {
      switch (polygon.properties.GEOID.length) {
        case 7: // the polygon is a city/place
          return "lightblue";
        case 5: // the polygon is a county
          return "blue";
        case 2: // the polygon is a state
          return "darkblue";
        default:
          return "blue"; // ??
      }
    },
    /*
     * Formats an Address in this style:
     * AddrLine1
     * AddrLine2
     * AddrLine3
     * City, County, StateProvince ZipPostalCode
     */
    getAHJOfficeAddress(ahj) {
      let address = ahj.Address;
      let result = "";
      if (address.AddrLine1.Value) result += address.AddrLine1.Value + "<br>";
      if (address.AddrLine2.Value) result += address.AddrLine2.Value + "<br>";
      if (address.AddrLine3.Value) result += address.AddrLine3.Value + "<br>";
      if (address.City.Value) result += address.City.Value + ", ";
      if (address.County.Value) result += address.County.Value + ", ";
      if (address.StateProvince.Value) result += address.StateProvince.Value + " ";
      if (address.ZipPostalCode.Value) result += address.ZipPostalCode.Value;
      return result;
    },
    /**
     * Removes all markers from the map
     */
    resetLeafletMapLayers() {
      if (this.polygonLayer !== null) {
        this.polygonLayer.removeFrom(this.leafletMap);
        this.polygonLayer = null;
      }
      if (this.currSearchMarker !== null) {
        this.leafletMap.removeLayer(this.currSearchMarker);
        this.currSearchMarker = null;
      }
      this.markerLayerGroup.clearLayers();
    },
    /**
     * Resets the map to the default focus and zoom
     */
    resetMapView() {
      this.leafletMap.setView(constants.MAP_INIT_CENTER, constants.MAP_INIT_ZOOM);
    }
  },
  /*
   * Load the leaflet map when this component is mounted
   */
  mounted() {
    this.setupLeafletMap();
  },
  watch: {
    /**
     * Listener to indicate if a new search was made
     * @param newVal the new selected ahj, may be null
     */
    "$store.state.selectedAHJ": function(newVal) {
      if (newVal === null) { // selectedAHJ === null is flush-out value
        // new search was made, and selectedAHJ reset to null
        this.resetLeafletMapLayers();
        this.resetMapView();
        this.previousPolygonAPIPage = "";
      } else { // search is completed
        if (this.$store.state.apiData.results.Location["Latitude"]["Value"] !== null) { // check if a location/address/region was searched
          if (this.polygonLayer === null || this.$store.state.apiData['previous'] !== this.previousPolygonAPIPage) { // if first page or different page
            this.previousPolygonAPIPage = this.$store.state.apiData['previous']; // track current page
            this.resetLeafletMapLayers();
            this.updateMap(this.$store.state.apiData.results.ahjlist);
          } else {
            // there are multiple polygons on the map at once to select
            this.selectPolygon(newVal.AHJID.Value);
          }
        } else { // no location/address/region was search
          // there is one polygon at a time on the map
          this.resetLeafletMapLayers();
          this.updateMap([newVal]);
        }
      }
    },
    /**
     * Tells the map to resize when showing the table for the first time
     */
    "$store.state.showTable": function() {
      this.leafletMap.invalidateSize(true);
    },
    filterToggled : function(newVal){
      if (newVal){
        // Add drawing tools
        this.addDrawingTools();
      }
      else {
        // Remove drawing tools
        this.leafletMap.removeControl(this.controlLayer);
      }
    },
    /**
     * Clear the polygon/region drawn on the map when AHJSearchFilter's clear is clicked
     * @param newVal the saved polygon/region; if null, then means it was cleared
     */
    "$store.state.searchedGeoJSON": function(newVal) {
      if (newVal === null) {
        this.searchPolygonFeatureGroup.clearLayers();
      }
    }
  }
};
</script>

<style scoped>
#mapdiv {
  width: 100%;
  height: 100%;
}

::v-deep .leaflet-left .leaflet-control {
  margin-left: 292px;
  margin-top: 75px;
}

@media (max-width: 1100px){
#mapdiv {
  width: 100%;
  min-height: 60vh;
}
}
</style>
