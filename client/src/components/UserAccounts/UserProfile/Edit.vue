<template>
    <div>
        <p>Changed the <b>{{EditedField}}</b> field on {{ahjName}} AHJ's <b>{{EditedDataType}}</b> data.</p>
        <div class="flex">
            <p>Old Value: <span class="red">{{ActivityData.OldValue}}</span></p>
            <p>New Value: <span class="green">{{ActivityData.NewValue}}</span></p>
        </div>
        <div class="flex">
            <p> Status: 
                <b-icon icon="circle-fill" class="circle-icon" :class="StatusColor"></b-icon> 
                <span :class="StatusColor">{{Status}}</span>
            </p>
            <p>
                <span v-if="Status === 'Approved'">Approved by:</span> <span v-if="Status === 'Rejected'">Rejected by: </span>
                <span v-if="this.ActivityData.ApprovedBy">{{ReviewedByFullName}}</span>
            </p>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import constants from "../../../constants.js";
export default {
    data() {
        return {
            ahjName: ''
        }
    },
    props: ['ActivityData'],
    computed: {
        EditedField(){
            return this.SplitByCapital(this.ActivityData.SourceColumn);
        },
        EditedDataType(){
            return this.SplitByCapital(this.ActivityData.SourceTable);
        },
        Status(){
            if (this.ActivityData.ReviewStatus === 'A') return "Approved";
            else if (this.ActivityData.ReviewStatus === 'R') return "Rejected";
            return "Pending";
        },
        StatusColor(){
            if (this.ActivityData.ReviewStatus === 'A') return "green";
            else if (this.ActivityData.ReviewStatus === 'R') return "red";
            return "grey";
        },
        ReviewedByFullName() {
            return `${this.ActivityData.ApprovedBy.ContactID.FirstName.Value} ${this.ActivityData.ApprovedBy.ContactID.LastName.Value}`;
        },
        AHJName(){
            return this.ahjName;
        }
    },
    methods: {
        // reformats the field returned by the API such that there are spaces between capital letters.
        SplitByCapital(string){
            return string.replace(/([A-Z]+)/g, ' $1').trim();
        },
        // Finds the name of an AHJ given the AHJPK for that AHJ.
        FindAHJName(AHJPK){
            let headers = {};
            if (this.$store.getters.loggedIn) {
              headers.Authorization = this.$store.getters.authToken;
            }
            axios.get(`${constants.API_ENDPOINT}ahj-one/`,
                { params: { AHJPK: AHJPK },
                  headers: headers})
                .then(response => { this.ahjName = response.data.AHJName.Value })
                .catch(err => { console.log(err) });
        }
    },
    mounted(){
        this.FindAHJName(this.ActivityData.AHJPK);
    }
}
</script>

<style scoped>
.red {
    color: red;
}
.green {
    color: green;
}
.grey {
    color: grey;
}
.circle-icon {
    height: 0.8em;
    width: 0.8em;
    margin-right: 0.4em;
}
.row-element {
    margin-right: 5%;
}
.flex {
    display: flex;
    flex-wrap: wrap;
}

.flex > p:first-child {
    margin-right: 1em;
}

</style>