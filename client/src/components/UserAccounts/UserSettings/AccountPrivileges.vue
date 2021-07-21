<template>
    <div>
        <h1>Account Privileges</h1>
        <h4 id="ahj-jurisdiction-text">AHJs where your account can approve/reject edit requests:</h4>
        <template v-if="numAHJNames < MaintainedAHJsCount">
            <p>Loading AHJs...</p>
        </template>
        <template v-if="numAHJNames === MaintainedAHJsCount && MaintainedAHJs.length === 0">
            <p>None.</p>
        </template>
        <template v-else>
            <!-- If any AHJS matched the user's maintained AHJs, display the list here. -->
            <ul>
                <li v-for="ahjName in MaintainedAHJs" :key="ahjName">{{ahjName}}</li>
            </ul>
        </template>
        <h5 id="help-text">If your email's domain matches the email/URL domain associated with an AHJ, then in the future you should automatically gain edit access for that AHJ.
            For now, please contact ahjregistry@sunspec.org if you do not have permission to edit your AHJ.
        </h5>

    </div>
</template>

<script>
import axios from "axios";
import constants from "../../../constants.js";
export default {
    data() {
        return {
            ahjNames: [],
            numAHJNames: 0
        }
    },
    computed: {
        MaintainedAHJsCount(){
            return this.$store.getters.currentUserInfo.MaintainedAHJs.length;
        },
        MaintainedAHJs(){
            return this.ahjNames;
        }
    },
    methods: {
        // For each AHJPK in the user's maintainedAHJs list, find it's name then display it in the list.
        GetAHJNames(MaintainedAHJs){
            for (let ahjpk of MaintainedAHJs){
                axios.get(`${constants.API_ENDPOINT}ahj-one/`,
                    { params: { AHJPK: ahjpk },
                      headers: { Authorization: this.$store.getters.authToken }})
                    .then(response => {
                      this.numAHJNames++;
                      this.ahjNames.push(response.data.AHJName.Value);
                    });
            }
        }
    },
    mounted() {
      // If current user's info is not already loaded, then the store is fetching it (page reload).
      if (this.$store.getters.currentUserInfo){
          this.GetAHJNames(this.$store.getters.currentUserInfo.MaintainedAHJs);
      }
  },
  watch: {
      // If store had to call API to get user info, get the AHJ names now.
      '$store.state.currentUserInfo' : function(newval) {
        this.GetAHJNames(newval.MaintainedAHJs);
      }
  },
}
</script>

<style scoped>
#help-text {
    margin-top: 50px;
}
@media (max-width: 650px){
    h1 {
        font-size: 2rem;
        margin-bottom: 1em;
    }
    #help-text {
        font-size: 1rem;
    }
    #ahj-jurisdiction-text {
        font-size: 1.3rem;
    }
}
</style>