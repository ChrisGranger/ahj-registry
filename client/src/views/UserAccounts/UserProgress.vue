<template>
    <div class="progress-page-container">
        <div id="progress-page-module">
            <template v-if="this.profileInfoLoaded">
                <div id="progress-page-content">
                    <h1>Progress Dashboard</h1>
                    <!-- Basic stats section -->
                    <div id="account-stats-section">
                        <account-stat icon="images/Badges/icons/edits-submitted-icon.png" 
                            v-bind:stat="numSubmittedEdits"
                            statName="Edits Submitted"
                        ></account-stat>
                        <account-stat icon="images/Badges/icons/edits-accepted-icon.png" 
                            v-bind:stat="numAcceptedEdits"
                            statName="Edits Accepted"
                        ></account-stat>
                        <account-stat icon="images/Badges/icons/community-score-icon.png" 
                            v-bind:stat="communityScore"
                            statName="Community Score"
                        ></account-stat>
                        <account-stat icon="images/Badges/icons/api-usage-icon.png" 
                            v-bind:stat="apiCalls"
                            statName="API Calls"
                        ></account-stat>
                    </div>
                    <!-- Badges section -->
                    <h2>Badges</h2>
                    <div id="badges-section">
                        
                    <!-- Badge boundaries mark scores users must hit to get silver or gold badges (or a future badge above gold).-->
                        <badge-progress badgeName="Edits Accepted"
                        v-bind:badgeData="getBadgeData('edits-accepted', numAcceptedEdits, acceptedEditsBoundaries)"
                        ></badge-progress>
                        <badge-progress badgeName="Community Score"
                        v-bind:badgeData="getBadgeData('community-score', communityScore, communityScoreBoundaries)"
                        ></badge-progress>
                        <badge-progress badgeName="API Usage"
                        v-bind:badgeData="getBadgeData('api-usage', apiCalls, apiUsageBoundaries)"
                        ></badge-progress>
                    </div>
                </div>
            </template>
            <template v-else>
                <p>Loading...</p>
            </template>
        </div>
    </div>
</template>

<script>
import constants from "../../constants.js";
import AccountStat from "../../components/UserAccounts/UserProgress/AccountStat.vue";
import BadgeProgress from "../../components/UserAccounts/UserProgress/BadgeProgess.vue";

export default {
    data(){
        return {
            profileInfoLoaded: false,
        }
    },
    computed:{
        numSubmittedEdits(){
            return this.$store.state.currentUserInfo.SubmittedEdits;
        },
        numAcceptedEdits(){
            return this.$store.state.currentUserInfo.AcceptedEdits;
        },
        communityScore(){
            return constants.COMMUNITY_SCORE_FORMULA(this.$store.state.currentUserInfo.SubmittedEdits, this.$store.state.currentUserInfo.AcceptedEdits);
        },
        apiCalls(){
            return this.$store.state.currentUserInfo.NumAPICalls;
        },
        acceptedEditsBoundaries(){
            return constants.ACCEPTED_EDITS_BADGE_BOUNDARIES;
        },
        communityScoreBoundaries(){
            return constants.COMMUNITY_SCORE_BADGE_BOUNDARIES;
        },
        apiUsageBoundaries(){
            return constants.API_USAGE_BADGE_BOUNDARIES;
        },
    },
    methods: {
        // Returns the current badge and next badge a user can work towards given a user's score in this category
        getBadgeData(badgeType, badgeScore, badgeBoundaries) {
            let badgeData = {'score': badgeScore};
            if (badgeScore >= badgeBoundaries[1]) {
                badgeData.max =  badgeBoundaries[2];
                badgeData.currBadge = `images/Badges/${badgeType}/gold.png`;
                badgeData.nextBadge = `images/Badges/${badgeType}/gold-dark.png`;
            } else if (badgeScore >= badgeBoundaries[0]){
                badgeData.max =  badgeBoundaries[1];
                badgeData.currBadge = `images/Badges/${badgeType}/silver.png`;
                badgeData.nextBadge = `images/Badges/${badgeType}/gold-dark.png`;
            } else {
                badgeData.max =  badgeBoundaries[0];
                badgeData.currBadge = `images/Badges/${badgeType}/bronze.png`;
                badgeData.nextBadge = `images/Badges/${badgeType}/silver-dark.png`;
            }
            return badgeData;
        },
    },
    components: {
    "account-stat": AccountStat,
    "badge-progress": BadgeProgress
  },
  mounted() {
    // If we are logged in and already have the user's info, then fill out the page.
    if (this.$store.getters.currentUserInfo){
      this.profileInfoLoaded = true;
    }
  },
  watch: {
      // If we had to grab the logged-in user's info when we reloaded this page, then we watch here to execute functions that rely on 
      // the logged-in user's information.
      '$store.state.currentUserInfo' : function() {
          if (this.$store.state.currentUserInfo){
              this.profileInfoLoaded = true;
          }
      }
  },
}
</script>

<style scoped>
h1 {
    margin-bottom: 1.5em;
    font-size: 3rem;
}
h2 {
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 1em;
}

.progress-page-container {
    background-color: #f2f5f7;
}

#progress-page-module {
    width: 70%;
    min-height: 60em;
    margin: 3.2em auto;
    background-color: white;
    border: 1px solid #D3D3D3;
}

#progress-page-content {
    width: 80%;
    margin: 3.2em auto;
}

#account-stats-section {
    display: flex;
    justify-content: space-evenly;
    align-items: flex-end;
    margin: 0em auto 5em;
}

#badges-section {
    width: 90%;
    margin: 0em auto 5em;
}

#ranking-section {
    width: 100%;
    height: 30em;
    display: flex;
    padding-top: 2em;
}
@media (max-width: 1000px){
    #account-stats-section {
        display: grid;
        align-items: center;
        justify-items: center;
        justify-content: center;
        grid-template-columns: 25% 25%;
        grid-template-rows: 25% 25%;
        gap: 3.5em 3.5em;
    }
}

@media (max-width: 800px){
    h1 {
        font-size: 2.3rem;
        text-align: center;
    }
    h2 {
        font-size: 2rem;
        font-weight: 400;
    }
    #progress-page-module {
        width: 90%;
    }

    #progress-page-content {
        width: 90%;
    }
    #badges-section {
        width: 100%;
    }
}

</style>