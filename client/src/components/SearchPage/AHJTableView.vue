<template>
  <div class="ahj-public-list-container">
    <div class="ahj-public-list">
      <!-- Bootstrap vue table -->
      <b-table
        ref="selectableTable"
        class="ahj-table"
        selectable
        :select-mode="'single'"
        selected-variant=""
        @row-clicked="onRowClicked"
        hover
        outlined
        small
        :fields="fields"
        :items="apiData.results ? apiData.results.ahjlist : undefined"
        :busy="apiLoading"
        show-empty
      >
      <template #empty>
        <!-- Table is empty either due to backend problem or due to no AHJs matched the query. -->
        <div v-if="apiError" class="ahj-not-found-text">
          An error with loading the data has occurred. Please try again.
        </div>
        <div v-else>
          No AHJs Found
        </div>
      </template>
        <template #table-busy>
          <div class="text-center text-primary my-2">
            <b-spinner class="align-middle"></b-spinner>
            <strong>&nbsp; Loading...</strong>
          </div>
        </template>
        <!-- Show more button's logic -->
        <template v-slot:cell(more_info)="row">
          <b-button size="sm" @click="row.toggleDetails" class="mr-2">
            {{ row.detailsShowing ? "Hide" : "Show" }}
          </b-button>
        </template>
        <!-- content displayed in 'show more' section -->
        <template #row-details="row">
          <b-card>
          <b-row class="mb-2">
            <b-col sm="3" class="text-sm-right"><b>Address:</b></b-col>
            <b-col v-html="rowGetAHJAddress(row)"></b-col>
          </b-row>
          <b-row class="mb-2">
            <b-col sm="4" class="text-sm-right"><b>Learn more about this AHJ:</b></b-col>
            <b-col><b-button size="sm" @click="openWithTab({ name: 'view-ahj', params: { AHJID: row.item.AHJPK.Value }})" class="mr-2">More Details</b-button></b-col>
          </b-row>
          </b-card>
        </template>
      </b-table>
    </div>
  </div>
</template>


<script>
export default {
  data() {
    return {
      fields: [
        {
          key: "AHJCode.Value",
          label: "AHJ Code",
          thStyle: { width: "274px" },
          class: "text-center",
          thClass: ".col-field-styling"
        },
        {
          key: "AHJName.Value",
          label: "AHJ Name",
          thStyle: { width: "274px" },
          class: "text-center",
          thClass: ".col-field-styling"
        },
        {
          key: "Address.County.Value",
          label: "County",
          thStyle: { width: "274px" },
          class: "text-center",
          thClass: ".col-field-styling"
        },
        {
          key: "BuildingCode.Value",
          label: "Building Code",
          thStyle: { width: "274px" },
          class: "text-center",
          formatter: this.ahjCodeFormatter,
          thClass: ".col-field-styling"
        },
        {
          key: "ElectricCode.Value",
          label: "Electric Code",
          thStyle: { width: "274px" },
          class: "text-center",
          formatter: this.ahjCodeFormatter,
          thClass: ".col-field-styling"
        },
        {
          key: "FireCode.Value",
          label: "Fire Code",
          thStyle: { width: "274px" },
          class: "text-center",
          formatter: this.ahjCodeFormatter,
          thClass: ".col-field-styling"
        },
        {
          key: "ResidentialCode.Value",
          label: "Residential Code",
          thStyle: { width: "274px" },
          class: "text-center",
          formatter: this.ahjCodeFormatter,
          thClass: ".col-field-styling"
        },
        {
          key: "WindCode.Value",
          label: "Wind Code",
          thStyle: { width: "274px" },
          class: "text-center",
          formatter: this.ahjCodeFormatter,
          thClass: ".col-field-styling"
        },
        "more_info"
      ]
    };
  },
  computed: {
    apiData() {
      return this.$store.state.apiData;
    },
    apiLoading() {
      return this.$store.state.apiLoading;
    },
    apiError() {
      return this.$store.state.apiErrorInfo.status;
    }
  },
  methods: {
    // Likely unused method which also sends the user to the corresponding AHJ Page.
    AHJPageSwitch(ahj){
      this.$store.state.currentAHJ = ahj;
      this.$router.push('view-ahj');
    },
    // When a table row is clicked, we change the map's currently selected AHJ and its associated polygon.
    onRowClicked(rowItem) {
      this.$store.commit("setSelectedAHJ", rowItem);
    },
    ahjCodeFormatter(value) {
      if(value) {
        if (value === "NoSolarRegulations") {
          return "No Solar Regulations";
        } else if (value === "SpecialWindZone") {
          return "Special Wind Zone";
        }
        return value.substring(0, 4) + " " + value.substring(4);
      }
      return value;
    },
    // Turns address in OB format into a html-presentable format
    rowGetAHJAddress(row) {
      let address = row.item.Address;
      let result = '';
      result += address.AddrLine1.Value;
      result += ' ';
      result += address.AddrLine2.Value;
      result += ' ';
      result += address.AddrLine3.Value;
      if (result !== '  ') {
        result += '<br>';
      }
      result += address.City.Value;
      result += ' ';
      result += address.County.Value;
      result += ',';
      result += ' ';
      result += address.StateProvince.Value;
      result += ' ';
      result += address.ZipPostalCode.Value;
      return result;
    },
    // Highlights the table's row which corresponds to the passed in AHJ.
    selectRow(ahj) {
      if (!this.$store.state.apiLoading) {
        let ahjlist = this.$store.state.apiData.results.ahjlist;
        for (let i = 0; i < ahjlist.length; i++) {
          if (ahjlist[i].AHJID.Value === ahj.AHJID.Value) {
            this.$refs.selectableTable.selectRow(i);
          }
        }
      }
    },
    openWithTab(routeObj){
      let page = this.$router.resolve(routeObj);
      window.open(page.href,'_blank');
    }
  },
  watch: {
    // Whenever the selectedAHJ changes in another component (such as clicking on the map markers),
    // change the highlighted AHJ row in the table.
    "$store.state.selectedAHJ": function(newVal) {
      if (newVal !== null) {
        this.selectRow(newVal);
      }
    },
  }
};
</script>

<style scoped>
.ahj-public-list-container {
  height: 100%;
}

.ahj-public-list {
  height: 86vh;
  overflow-y: scroll;
}

#table-caption{
  font-size: 30em;
  caption-side: top;
  display: none;
}
.ahj-not-found-text{
  font-size: 1.3em;
  text-align: center;
}

@media (max-width: 1100px){
  .ahj-public-list {
    height: auto;
    overflow-y: scroll;
  }
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

::v-deep .table > tbody > tr.b-table-row-selected {
  border: 3px solid #85e9f2;
}

::v-deep .table.b-table.table-hover > tbody > tr:hover td {
  background-color: #e3fcf9;
}

::v-deep .table > tbody > tr:nth-child(odd){
  background-color: #fff2e5;
}

::v-deep .table > tbody > tr:nth-child(even) {
  background-color: #ffffff;
}
</style>
