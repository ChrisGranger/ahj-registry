<template>
  <div class="ahj-search-container">
    <div class="search-and-map ahj-search-filter">
      <ahj-search-filter ref="searchFilter" v-on:ToggleSearchFilter="ToggleSearchFilter($event)"></ahj-search-filter>
    </div>
    <div class="search-and-map ahj-search-map" id="ahj-search-map">
      <component-mapview v-bind:filterToggled="this.filterToggled"></component-mapview>
    </div>
    <div class="ahj-table-sidebar" v-show="$store.state.showTable">
      <div class="table-info">
        <component-ahj-table-result-info class="ahj-table-result-info"></component-ahj-table-result-info>
        <component-ahj-table-pagination class="ahj-table-pagination"></component-ahj-table-pagination>
      </div>
      <component-ahj-table-view></component-ahj-table-view>
    </div>
  </div>
</template>

<script>
import MapView from "../components/SearchPage/MapView.vue";
import AHJTableView from "../components/SearchPage/AHJTableView.vue";
import AHJSearchPageFilter from "../components/SearchPage/AHJSearchPageFilter.vue";
import AHJTablePagination from "../components/SearchPage/AHJTablePagination";
import AHJTableResultInfo from "../components/SearchPage/AHJTableResultInfo";
import "intro.js/minified/introjs.min.css";
const introJs = require('intro.js');
export default {
  data() {
    return {
      introStep: 0,
      runningTour: false,
      tutorial: null,
      filterToggled: true
    }
  },
  created() { // called before 'mounted' is called for child components
    // hide the search results table on page load
    this.$store.commit("setShowTable", false);
  },
  mounted() {
    if (this.$route.query.tutorial == 1){
      this.StartTutorial();
    }
  },
  beforeDestroy() {
    if (this.runningTour) {
      this.tutorial.exit();
    }
  },
  methods: {
    ToggleSearchFilter(isToggled) {
      this.filterToggled = isToggled;
    },
    StartTutorial() {
    let that = this;
    // attach click listener for the tour
    let clickEventLister = () => window.dispatchEvent(new Event(('resize')));
    document
        .querySelector('.ahj-search-filter')
        .addEventListener('click', clickEventLister);
    this.runningTour = true;
    this.tutorial = introJs();
        this.tutorial.setOptions({
          showStepNumbers: true,
          exitOnOverlayClick: false,
          showBullets: false,
          steps: [{
            title: 'Welcome',
            intro: '<p>Welcome, to the AHJ Registry! Here you can find all' +
                ' of the information necessary to successfuly apply for and receive ' +
                'a construction permit in the USA.</p>' +
                '<p>Let\'s take a quick tour through the search tool. For more information ' +
                'about the project, please visit our <a href="/#/about">About page.</a></p>'
          },{
            element: document.querySelector('.search-filter-form'),
            position: 'right',
            title: 'Finding Information',
            intro: '<p>Our feature-rich search tool helps users quickly find AHJ ' +
                'information related to different geographical regions.</p>' +
                '<p>Let\'s see how to best use it!</p>'
          },{
            element: document.querySelector('.search-filter-form  .search-field-group'),
            title: 'Addresses and Coordinates',
            position: 'right',
            intro: '<p>The search bar allows you to type any valid address or pair of' +
                ' latitude longitude coordinates to find AHJs who have jurisdiction' +
                ' over this area.</p> <p>For example, let\'s search with SunSpec\'s address.</p>'
          },{
            element: document.querySelector('.search-filter-form'),
            title: 'Try It Yourself!',
            position: 'right',
            intro: '<p>The best learning comes when you try yourself. Enter an address, or ' +
                'use the preloaded query, so we can see how to interpret search  results.</p>' +
                '<p>To continue, <b>click the search button.</b></p>'
          },{
            element: document.querySelector('.search-and-map'),
            title: 'Visualizing the Results',
            intro: '<p>Our interactive map is a great way to quickly see your search results.</p>' +
                '<p>Here\'s a quick guide to navigating this information:</p>' +
                '<ul>' +
                '<li>Your searched address is marked by a gray marker with an empty circle.</li>' +
                '<li>AHJ office locations are represented as blue markers with a building inside.</li>' +
                '<li>The red polygon shows the jurisdiction area for the currently selected AHJ. ' +
                'By default, the currently selected AHJ is the first entry in our table.</li>' +
                '</ul>'
          },{
            element: document.querySelector('.ahj-table-sidebar'),
            title: 'Quantitative Information',
            intro: '<p>Our table sidebar provides greater detail about the AHJs that matched your search. ' +
                'Each row contains high-level permitting information about a specific AHJ and has ' +
                'links to their specific AHJ page here on the registry. ' +
                'These AHJ pages contain more information about the AHJs such as contact information, permit submission methods, and fee structures. </p>' +
                '<p>When a large number of search results are found you can flip through table pages' +
                ' and download the results for batch processing.</p>'
          },{
            element: document.querySelector('.search-filter-form'),
            title: 'Advanced Searching',
            position: 'right',
            intro: '<p>Sometimes, a simple address search is not enough. ' +
                'Click on <em>show search options and filters</em> to see additional search features.</p>' +
                '<p>These advanced filters are great for those who need to find AHJs spanning a large' +
                ' region, or inversely, to find regions that have certain building requirements.</p>' +
                '<p>Take a second to look through the available search options for advanced filtering.</p>'
          },{
            title: 'Thank You',
            intro: '<p>The AHJ Registry has many exciting features for you to discover ' +
                'and we thank you for taking the time to work through this tutorial.</p>' +
                '<p>We hope you find the information that you\'re looking for. Details about the ' +
                'registry can be found on our <a href="/#/about">About Page</a>' +
                ' and additional tutorials will be coming out shortly!</p>'
          },]
        })
        .onbeforechange(function() {
          that.introStep++;
          switch (that.introStep) {
            case 4: // remove next button to prompt user to click 'Next'
              document.querySelector('.introjs-nextbutton').style.display = 'none';
              break;
          }
        }).onchange(function(element) {
      switch (element.id) {
        case "search-group": // fill in the search with an example query
          that.$refs.searchFilter.setDemoAddress();
          break;
      }
    })
        .onexit(() => {
          // remove click listener
          document
              .querySelector('.ahj-search-filter')
              .removeEventListener('click', clickEventLister);
          that.runningTour = false;
        })
        .start();
    }
  },
  components: {
    "ahj-search-filter": AHJSearchPageFilter,
    "component-mapview": MapView,
    "component-ahj-table-result-info": AHJTableResultInfo,
    "component-ahj-table-pagination": AHJTablePagination,
    "component-ahj-table-view": AHJTableView
  },
  watch: {
    /**
     * Listener to make the tutorial's 'Next' button reappear if search was made
     * @param newVal
     */
    '$store.state.showTable': function(newVal) {
      if (newVal && this.runningTour) {
        document.querySelector('.introjs-nextbutton').style.display = '';
      }
    }
  }
};
</script>

<style scoped>
.ahj-search-container {
  display: grid;
  grid-template-columns: auto fit-content(40%);
}

.ahj-search-filter {
  grid-column: 1;
  grid-row: 1 / 3;
}

.ahj-search-map {
  grid-column: 1;
  grid-row: 1 / 3;
}

.ahj-table-sidebar {
  grid-column: 2;
  grid-row: 1 / span 2;
  padding-left: 1em;
}

.table-info {
  display: grid;
  background: white;
}

.ahj-table-result-info {
  grid-column: 1;
}

.ahj-table-pagination {
  grid-column: 2;
  text-align: right;
}
@media (max-width: 1100px){
  .ahj-search-container {
    grid-template-rows: auto fit-content(40%);
  }

  .ahj-search-filter {
    grid-row: 1 / 2;
  }

  .ahj-search-map {
    grid-row: 1 / 2;
  }

  .ahj-table-sidebar {
    grid-column: 1;
    grid-row: 2 / 3;
  }
}
</style>
