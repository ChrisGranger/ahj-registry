<template>
    <div class="search-filter-form" v-if="!isMobile || filterToggled">
      <form @submit.prevent>
        <h1>Search by Address or Coordinates</h1>
        <div class="form-group search-field-group" id="search-group">
          <input id="search-bar-input" type="text" class="form-control search-input" v-model="parameters.Address"
                placeholder="Address or Coordinates" @keydown.enter="updateQuery"/>
          <b-icon icon="info-circle-fill" scale="2" variant="info" id="info-tooltip-target"></b-icon>
          <b-tooltip target="info-tooltip-target" triggers="click hover" placement="right" variant="light">
            * Returns the presiding AHJs over the searched address. <br>
            * Mandatory coordinate format: ±d ±d
          </b-tooltip>
        </div>
        <div id='drop' class="form-group dropdown-content">
          <div class='options' @click='toggleDropdown("bcdrop", "plusbutton")'>
            <i id='plusbutton' class="fas fa-plus"></i>
            Building Codes
          </div>
          <div id='bcdrop' class='dropdown-content building-code-dropdown-lists'>
            <div class='building-code-option'>
              <h2>Building Codes</h2>
              <b-form-select v-model="parameters.BuildingCode" :options="choiceFields.AHJ.BuildingCode" class="form-select" multiple
                          :select-size="2"/>
            </div>
            <div class='building-code-option'>
              <h2>Electric Codes</h2>
              <b-form-select v-model="parameters.ElectricCode" :options="choiceFields.AHJ.ElectricCode" class="form-select" multiple
                            :select-size="2"/>
            </div>
            <div class='building-code-option'>
              <h2>Fire Codes</h2>
              <b-form-select v-model="parameters.FireCode" :options="choiceFields.AHJ.FireCode" class="form-select" multiple :select-size="2"/>
            </div>
            <div class='building-code-option'>
              <h2>Residential Codes</h2>
              <b-form-select v-model="parameters.ResidentialCode" :options="choiceFields.AHJ.ResidentialCode" class="form-select" multiple
                            :select-size="2"/>
            </div>
            <div class='building-code-option'>
              <h2>Wind Codes</h2>
              <b-form-select v-model="parameters.WindCode" :options="choiceFields.AHJ.WindCode" class="form-select" multiple :select-size="2"/>
            </div>
          </div>
          <div class='options' @click='toggleDropdown("search-options-drop", "plusbuttonAHJ")'>
            <i id='plusbuttonAHJ' class="fas fa-plus"></i>
            More Search Options
          </div>
          <div id="search-options-drop" class='dropdown-content'>
            <input id="ahjname" type="text" class="form-control search-input" v-model="parameters.AHJName"
                  placeholder="AHJ Name"/>
            <input id="ahjcode" type="text" class="form-control search-input" v-model="parameters.AHJCode"
                  placeholder="AHJ Code"/>
            <b-form-select v-model="parameters.AHJLevelCode" class="search-input" :options="choiceFields.AHJ.AHJLevelCode" />
            <input id="stateprovince" type="text" class="form-control search-input" v-model="parameters.StateProvince"
                  placeholder="State/Province"/>
            <input id="ahjid" type="text" class="form-control search-input" v-model="parameters.AHJID"
                  placeholder="AHJ ID"/>
          </div>
        </div>
        <div class="button-group">
          <button type="button" class="btn btn-primary" @click="clearFilters">Clear</button>
          <button type="button" class="btn btn-primary" @click="copyLinkToClipboard">
            <i width=12 class="search-icon far fa-copy"></i>
            Link
          </button>
          <button type="button" class="btn btn-primary" @click="updateQuery">
            <i width=12 class="search-icon fas fa-search"></i>
            Search
          </button>
        </div>
          <div id='showbutton' class="show-more-toggle" @click='show'>
          <i width=12 class="arrow-icon fas fa-chevron-down"></i>
          <h2>Show search options and filters</h2>
          </div>
          <div id='hidebutton' class='show-more-toggle dropdown-hide' @click='show'>
            <i width=12 class="arrow-icon fas fa-chevron-up"></i>
            <h2>Hide</h2>
          </div>
      </form>
    </div>
    <div class="search-filter-form collapsed" v-else>
      <div class="show-more-toggle">
        <i width=12 class="arrow-icon fas fa-chevron-down"></i>
        <h2 @click="SearchFilterToggled()" style="cursor: pointer;">Reopen Search Bar</h2>
      </div>
    </div>
</template>

<script>
import constants from "../../constants";

export default {
  data() {
    return {
      parameters: this.getParametersObject(),
      choiceFields: constants.CHOICE_FIELDS,
      filterToggled: true,
      windowWidth: window.innerWidth
    };
  },
  computed: {
    isMobile() {
      return this.windowWidth < 600;
    }
  },
  mounted() {
    // reset search filters
    this.clearFilters();
    // Create window resize listener
    this.$nextTick(() => {
      window.addEventListener('resize', this.onResize);
    });
    // Check if a search was given in the query params
    if (this.setQueryFromObject(this.$route.query)) {
      this.updateQuery();
    }
  },
  beforeDestroy() { 
    window.removeEventListener('resize', this.onResize); 
  },
  methods: {
    onResize() {
      this.windowWidth = window.innerWidth;
    },
    /**
     * Helper for search page tutorial to fill in search query.
     * It is not used in this Vue component, but by its parent component.
     */
    setDemoAddress() {
      this.parameters.Address = '4040 Moorpark Ave. Suite 110, San Jose, CA, 95117';
    },
    /**
     * Composes a new search query with parameters the user has inputted into the form.
     * Calls the backend's API once a query is formed.
     */
    updateQuery() {
      let queryObject = {};
      Object.keys(this.parameters).forEach(key => {
        if(this.parameters[key].length > 0) {
          queryObject[key] = this.parameters[key];
        }
      });
      this.SearchFilterToggled();
      this.$store.commit("setSelectedAHJ", null);
      this.$store.commit("callAPI", queryObject);
    },
    SearchFilterToggled() {
      this.filterToggled = !this.filterToggled;
      if (this.isMobile){
        this.$emit('ToggleSearchFilter', this.filterToggled);
      }
    },
    /**
     * Clear the search query inputs
     */
    clearFilters() {
      this.parameters = this.getParametersObject();
      this.$store.commit('setSearchGeoJSON', null);
    },
    /**
     * Returns object for storing search parameters
     */
    getParametersObject() {
      return {
        AHJName: "",
        AHJCode: "",
        AHJLevelCode: "",
        AHJID: "",
        Address: "", // Location (latlng) searches are done through the Address field
        BuildingCode: [],
        ElectricCode: [],
        FireCode: [],
        ResidentialCode: [],
        WindCode: [],
        StateProvince: ""
      };
    },
    /**
     * Create a parameterized url for containing all filled search parameters
     */
    getParameterizedURL() {
      let parameters = this.parameters;
      let geojson = this.$store.state.searchedGeoJSON;
      if (geojson) {
        parameters['GeoJSON'] = encodeURIComponent(JSON.stringify(geojson));
      }
      let currentURL = window.location.href.split('?')[0];
      let queryString = Object.keys(this.parameters)
          .filter(k => {
            let v = this.parameters[k];
            return v !== '' && (Array.isArray(v) ? v.filter(x => x !== '').length !== 0 : true)
          })
          .map(k => {
            let v = this.parameters[k];
            v = Array.isArray(v) ? v : [v];
            return `${k}=${v.join(',')}`;
          })
          .join('&');
      return `${currentURL}?${queryString}`;
    },
    /**
     * Sets the parameters of the search using the values
     * of the keys in the object that match the parameter names.
     * @returns boolean if any parameters were set.
     */
    setQueryFromObject(obj) {
      let parameters = Object.keys(this.parameters)
          .concat('GeoJSON')
          .filter(k => Object.prototype.hasOwnProperty.call(obj, k));
      let setParameters = parameters.length > 0;
      if (setParameters) {
        parameters.filter(k => Array.isArray(this.parameters[k]))
        .forEach(k => {
          let choices = this.choiceFields.AHJ[k]
              .map(a => a.value);
          this.parameters[k] = obj[k]
              .split(',')
              .filter(v => choices.includes(v));
        });
        parameters.filter(k => k !== 'GeoJSON' && !Array.isArray(this.parameters[k]))
        .forEach(k => this.parameters[k] = obj[k]);
        if (obj['GeoJSON']) {
          try {
            let geojson = JSON.parse(decodeURIComponent(obj['GeoJSON']));
            this.$store.commit('setSearchGeoJSON', geojson);
          } catch (err) {
            console.log('Invalid JSON in GeoJSON query parameter');
          }
        }
      }
      return setParameters;
    },
    /**
     * Helper to write parameterized url to user's clipboard
     */
    copyLinkToClipboard() {
      navigator.clipboard.writeText(this.getParameterizedURL())
          .then(() => { /* success */ })
          .catch(() => { /* failed */ });
    },
    /**
     * Toggles the visibility of the additional filters and search options
     */
    show() {
      let elems = ['drop', 'showbutton', 'hidebutton'].map(id => document.getElementById(id));
      ['show', 'dropdown-hide', 'dropdown-hide'].forEach((c, i) => elems[i].classList.toggle(c));
    },
    /**
     * Toggles the visibility of dropdown
     */
    toggleDropdown(dropdownId, iconId) {
      let content = document.getElementById(dropdownId);
      let icon = document.getElementById(iconId);
      let alreadyActive = content.classList.contains('active');
      let activeContent = [...document.getElementsByClassName('active')];
      let activeIcons = [...document.getElementsByClassName('fa-minus')];
      activeContent.forEach(c => this.setClassesOnElem(c, [], ['active', 'show']));
      activeIcons.forEach(i => this.setClassesOnElem(i, ['fa-plus'], ['fa-minus']));
      if (!alreadyActive) {
        this.setClassesOnElem(content, ['active', 'show'], [])
        this.setClassesOnElem(icon, ['fa-minus'], ['fa-plus'])
      }
    },
    /**
     * For the given element, adds and removes the specified classes
     * from its classList.
     * @param elem the element with a classList
     * @param toAdd the classes to add
     * @param toRemove the classes to remove
     */
    setClassesOnElem(elem, toAdd, toRemove) {
      toAdd.forEach(c => elem.classList.add(c));
      toRemove.forEach(c => elem.classList.remove(c));
    }
  },
  watch: {
    isMobile(newValue) {
      if (!this.filterToggled) {
        this.$emit('ToggleSearchFilter', !newValue);
      }
    }
  },
};
</script>

<style scoped>
h1 {
  font-size: 20px;
  color: #4b4e52;
  font-weight: bold;
  display: block;
  margin: 0 auto;
  text-align: center;
}
h2 {
  font-size: 14px;
  font-weight: bold;
  text-align: center;
}
.search-filter-form {
  position: relative;
  padding-top: 5px;
  top: 5%;
  left: 0.5%;
  z-index: 500;
  width: 280px;
  background: white;
  border: 1px solid black;
  border-radius: 8px;
  font-family: "Open Sans";
}
.collapsed {
  top: 0%;
  width: 200px;
}
.form-group {
  display: block;
}
button {
  margin: 0px 10px 15px 0px;
}
.button-group {
  display: flex;
  justify-content: flex-end;
}
.btn-primary,
.btn-primary:active,
.btn-primary:visited,
.btn-primary:focus,
.btn-primary:disabled {
  background-color: white;
  border-color: #4b4e52;
  color: #4b4e52;
  border-radius: 20px;
}
.btn-primary:hover {
  background-color: #eeeeee;
  color: #4b4e52;
  border-color: #4b4e52;
}
.search-field-group {
  display: flex;
  align-items: center;
  margin-top: 0.5em;
  justify-content: space-between;
}
#search-bar-input {
  flex: 4;
}
#info-tooltip-target {
  flex: 1;
}
.search-input {
  width: 95%;
  display: block;
  margin: 0 auto;
  border-radius: 20px;
  margin-bottom: 0px;
  font-size:14px;
}
.dropdown-content {
  display: none;
}
.show {
  display: block;
}
.dropdown-hide {
  display: none !important;
}
.options {
  margin-left: 1em;
  font-size: 1em;
  cursor: pointer;
  color: #4b4e52;
}
.options:hover {
  color: black;
}
.form-control {
  margin: 0.2em;
}
.building-code-dropdown-lists {
  margin-left: 1em;
  font-size: 1em;
  color: #4b4e52;
}
.building-code-option {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 0.5em 0.5em 0em 0em;
}
.building-code-option > h2 {
  flex: 0.35;
  margin-right: 0.5em;
}
.building-code-option > .form-select {
  flex: 0.65;
  font-size: 14px;
  padding: 5px;
}
.api-settings-input-title {
  display: flex;
  align-items: center;
  justify-content: center;
}
.api-settings-input-title > h2 {
  margin: 0.5em;
}
.show-more-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #8d8d8d;
}
.show-more-toggle:hover {
  color: #5c5c5c;
}
.show-more-toggle > h2 {
  margin-top: 7px;
}
.show-more-toggle > i {
  margin-left: 10px;
  margin-right: 10px;
}
.arrow-icon {
  display: block;
  width: 12px;
}
.search-icon {
  color: #5D98DD;
}
.info-icon {
  color: #28679E;
}
</style>
