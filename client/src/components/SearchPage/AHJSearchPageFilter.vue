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
  <!--        <div class='options' @click='showapisettings'>-->
  <!--          <i id='plusbuttonAPI' class="fas fa-plus"></i>-->
  <!--          API Settings-->
  <!--        </div>-->
  <!--        <div id='apisettings' class='dropdown-content'>-->
  <!--          <div class='api-settings-input'>-->
  <!--            <div class='api-settings-input-title'>-->
  <!--              <h2>View Edits As</h2>-->
  <!--              <b-icon icon="info-circle-fill" class="view-edits-info-icon" scale="1" variant="info" id="info-tooltip-target2"></b-icon>-->
  <!--              <b-tooltip target="info-tooltip-target2" triggers="hover" placement="right" variant="light">-->
  <!--                <b>Latest Edits</b> includes unconfirmed edits provided by the community. <br>-->
  <!--                <b>Confirmed Edits</b> only include edits confirmed by AHJs.-->
  <!--              </b-tooltip>-->
  <!--            </div>-->
  <!--            <b-form-select v-model="parameters.view" class="search-input" :options="choiceFields.APIEditViewMode" />-->
  <!--          </div>-->
  <!--        </div>-->
          <div class='options' @click='showbc'>
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
          <div class='options' @click='showMoreSearchOptions'>
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
      parameters: {
        view: "latest",
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
        StateProvince: "",
        callerID: 'searchpagefilter'
      },
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
    })
    // Check if a search was given in the query params; if so, search by it (run tutorial when tutorial is non null and 1, else )
    if (this.$route.query.tutorial != 1 && Object.keys(this.$route.query).length !== 0) {
      Object.keys(this.parameters)
          .filter(a => a !== 'callerID') // this should not be changed by the user
          .forEach(key => {
            let paramValue = this.$route.query[key];
            if (paramValue) {
              if (Array.isArray(this.parameters[key])) {
                let choices = this.choiceFields.AHJ[key].map(a => a.value);
                this.parameters[key] = paramValue
                    .split(',')
                    .filter(v => choices.includes(v));
              } else {
                this.parameters[key] = paramValue; // set the search values
              }
            }
          });
      if (this.$route.query['Location']) {
        this.parameters['Address'] = this.$route.query['Location']; // send location queries through address field
      }
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
      this.parameters = {
        view: "latest",
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
        StateProvince: "",
        callerID: 'searchpagefilter'
      };
      this.$store.commit('setSearchGeoJSON', null);
    },
    /**
     * Create a parameterized url for containing all filled search parameters
     */
    getParameterizedURL() {
      let currentURL = window.location.href;
      if (currentURL.indexOf("?") > 0) {
        currentURL = currentURL.substring(0, currentURL.indexOf("?"));
      }
      let queryString = "";
      Object.keys(this.parameters)
          .filter(a => a !== 'callerID') // this should not be set by users
          .forEach(key => {
            if(this.parameters[key] !== ""){
              if(Array.isArray(this.parameters[key])){
                if(this.parameters[key].length > 0 && this.parameters[key][0] !== ""){
                  queryString += key + "=" + this.parameters[key].join(',');
                  queryString += "&";
                }
              } else {
                queryString += key + "=" + this.parameters[key] + "&";
              }
            }
          });
      if (queryString) {
        currentURL += '?' + queryString;
      }
      currentURL = currentURL.slice(0,-1);
      return currentURL;
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
    show(){
      document.getElementById('drop').classList.toggle('show')
      document.getElementById('showbutton').classList.toggle('dropdown-hide')
      document.getElementById('hidebutton').classList.toggle('dropdown-hide')
    },
    /**
     * Toggles the visibility of the api settings dropdown
     */
    showapisettings() {
      let currContent = document.getElementsByClassName("active");
      if (currContent.length > 0 && currContent[0].id !== 'apisettings'){
        this.closeActiveSettings();
      }
      let icon = document.getElementById('plusbuttonAPI');
      let content = document.getElementById('apisettings');
      this.toggleSettings(icon,content);
    },
    /**
     * Toggles the visibility of the building codes dropdown
     */
    showbc(){
      let currContent = document.getElementsByClassName("active");
      // Covers case if they click on this dropdown while it's active.
      if (currContent.length > 0 && currContent[0].id !== 'bcdrop'){
        this.closeActiveSettings();
      }
      let icon = document.getElementById('plusbutton');
      let content = document.getElementById('bcdrop');
      this.toggleSettings(icon,content);
    },
    /**
     * Toggles the visibility of the additional search options dropdown
     */
    showMoreSearchOptions(){
      let currContent = document.getElementsByClassName("active");
      if (currContent.length > 0 && currContent[0].id !== 'search-options-drop'){
        this.closeActiveSettings();
      }
      let icon = document.getElementById('plusbuttonAHJ');
      let content = document.getElementById('search-options-drop');
      this.toggleSettings(icon,content);
    },
    /**
     * Toggles the visibility and +/- icon of a dropdown.
     */
    toggleSettings(icon, content){
      content.classList.toggle('show');
      content.classList.toggle('active');
      icon.classList.toggle('fa-plus');
      icon.classList.toggle('fa-minus');
    },
    /**
     * Closes the currently active dropdown.
     * Called when user clicks on a dropdown that is currently active.
     */
    closeActiveSettings(){
      // Only 1 option should have a minus and the "show" and "active" attribute. We will toggle these off.
      var icon = document.getElementsByClassName("fa-minus");
      var dropdownContent = document.getElementsByClassName("active")[0];
      if (icon.length > 0){
        icon[0].classList.toggle('fa-plus');
        icon[0].classList.toggle('fa-minus');
        dropdownContent.classList.toggle('active');
        dropdownContent.classList.toggle('show');
      }
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
