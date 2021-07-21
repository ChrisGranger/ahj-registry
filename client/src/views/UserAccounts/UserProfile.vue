<template>
    <div class="user-page">
        <div id="user-page-container" v-if="userInfoLoaded">
                <div id='user-header'>
                    <div id="banner-section">
                        <img id='banner-image' src="../../assets/images/background-image.jpeg"/>
                        <div id="badges-container">
                            <div class="badges">
                                <img class="badge" :src="require('@/assets/' + acceptedEditsBadge + '')" title="Accepted Edits Badge">
                                <img class="badge" :src="require('@/assets/' + communityScoreBadge + '')" title="Community Score Badge">
                                <img class="badge" :src="require('@/assets/' + apiUsageBadge + '')" title="API Usage Badge">
                            </div>
                        </div>
                    </div>
                    <img id='user-image' src="../../assets/images/profile-image-default.jpeg" />
                    <div id="header-content">
                        <div id="header-content-left">
                            <div>
                                <template v-if="fullName !== ' '">
                                    <h2 class="profile-name"><b>{{fullName}}</b></h2>
                                </template>
                                <template v-else>
                                    <h2 class="profile-name"><b>{{username}}</b></h2>
                                </template>
                            </div>
                            <hr>
                            <h3 :class="contributorColor">{{contributorText}} Contributor</h3>
                            <div id="user-work-section" v-if="companyAffiliation !== null">
                                <h4 style="margin-right:5%;">{{companyAffiliation}}</h4>
                                <h4 style="margin-right:5%;" v-if="title"> - </h4>
                                <h4 v-if="title">{{title}}</h4>
                            </div>
                            <div class="user-stats-container">
                                <h6 id="user-stat-edits-submitted">Submitted edits: {{numSubmittedEdits}}</h6>
                                <h6 id="user-stat-edits-accepted">Accepted edits: {{numAcceptedEdits}}</h6>
                                <h6 id="user-stat-community-score">Community Score: {{communityScore}}</h6>
                                <h6 id="user-stat-api-usage"># of API Calls: {{apiCalls}}</h6>
                            </div>
                        </div>
                        <div id="header-content-right">
                            <div id="header-buttons-right">
                                <b-button v-b-modal.user-modal size="sm" class="contact-info-button" variant="outline-primary" busy="True">Contact Info</b-button>
                                <b-modal id="user-modal">
                                    <template #modal-title>
                                        {{`${fullName}'s Contact Info`}}
                                    </template>
                                    {{`Email: ${email}`}} <br>
                                    {{`Phone: ${phone}`}} <br>
                                    {{`Preferred Contact Method: ${preferredContact}`}}
                                </b-modal>
                                <b-button v-if="this.$store.getters.loggedIn && username === this.$store.getters.currentUserInfo.Username" class="button" @click="$router.push({ name: 'settings'})" pill variant="primary">
                                    Edit Profile
                                </b-button>
                            </div>
                        </div>
                    </div>
                </div>
                <div id="user-about">
                    <h2 class='section-header'>About</h2>
                    <hr>
                    <template v-if="personalBio !== null && personalBio !== ''">
                        <p class="about-text">{{personalBio}}</p>
                    </template>
                    <template v-else>
                        <p class="about-text alternative-text">User has not filled their about section.</p>
                    </template>
                </div>
                <div id="user-feed">
                    <h2 class='section-header'>Feed</h2>
                    <hr>
                    <b-button-group id="user-feed-button-container">
                        <b-button variant="outline-secondary" @click="GetUserActivity('Edit')"> Edits </b-button>
                        <b-button variant="outline-secondary" @click="GetUserActivity('Comment')"> Comments </b-button>
                    </b-button-group>
                    <template v-if="activities.length > 0">
                    <!--Generate an activity-entry component for all edits a user has made. -->
                        <template v-if="FeedActivity === 'Edit'">
                            <activity-entry 
                                v-for="activity in (activities || []).slice(0, 10)" 
                                v-bind:key="activity.EditID" 
                                v-bind:UserData="activity.ChangedBy" 
                                v-bind:ActivityType="FeedActivity" 
                                v-bind:ActivityData="activity"
                                v-bind:Photo="photo">
                            </activity-entry>
                        </template>
                        <!--Generate an activity-entry component for all comments a user has made. -->
                        <template v-else>
                            <activity-entry 
                                v-for="activity in (activities || []).slice(0, 10)" 
                                v-bind:key="activity.CommentID.Value" 
                                v-bind:UserData="ProfileDataObj" 
                                v-bind:ActivityType="FeedActivity" 
                                v-bind:ActivityData="activity"
                                v-bind:Photo="photo">
                            </activity-entry>
                        </template>
                    </template>
                    <template v-else>
                        <div v-if="this.gettingUserActivity">
                            <p class="alternative-text">Getting {{FeedActivity}} history...</p>
                        </div>
                        <div v-else>
                            <p class="alternative-text">User has no {{FeedActivity}} history</p>
                        </div>
                    </template>
                </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import constants from "../../constants.js";
import ActivityEntry from "../../components/UserAccounts/UserProfile/ActivityEntry.vue";

export default {
    // Computed properties relevant to a user profile for easy access in the above template.
    computed: {
        userID(){
            return this.ProfileData['UserID']; 
        },
        photo(){
            return this.ProfileData['Photo']; 
        },
        fullName(){
            return this.ProfileData['ContactID']['FirstName']['Value'] + " " + this.ProfileData['ContactID']['LastName']['Value']; 
        },
        email(){
            return this.ProfileData['Email'];
        },
        username(){
            return this.ProfileData['Username'];
        },
        phone(){
            return this.ProfileData['ContactID']['WorkPhone']['Value'];
        },
        preferredContact(){
            return this.ProfileData['ContactID']['PreferredContactMethod']['Value'];
        },
        url(){
            return this.ProfileData['ContactID']['URL']['Value'];
        },
        numReviewsDone(){
            return this.ProfileData['NumReviewsDone'];
        },
        numAcceptedEdits(){
            return this.ProfileData['AcceptedEdits'];
        },
        numSubmittedEdits(){
            return this.ProfileData['SubmittedEdits'];
        },
        communityScore(){
            return this.ProfileData['CommunityScore'];
        },
        apiCalls(){
            return 0; // Change when we begin tracking API calls with new schema
        },
        personalBio(){
            return this.ProfileData['PersonalBio'];
        },
        companyAffiliation(){
            return this.ProfileData['CompanyAffiliation'];
        },
        title(){
            return this.ProfileData['ContactID']['Title'].Value;
        },
        location(){
            return this.ProfileData['IsPeerReviewer'];
        },
        contributorText(){
            if (this.goldBadgeCount > 0) return 'Gold';
            else if (this.silverBadgeCount > 0) return 'Silver';
            else return 'Bronze';
        },
        contributorColor() {
            if (this.goldBadgeCount > 0) return 'gold';
            else if (this.silverBadgeCount > 0) return 'silver';
            else return 'bronze';
        },
        ProfileDataObj(){
            return this.ProfileData;
        },
    },
    data() {
        return {
            ProfileData: {},
            userInfoLoaded: false,
            activities: [],
            FeedActivity: 'Edit',
            gettingUserActivity: true,
            uploadedApplication: null,
            applicationStatus: null,
            // Badge counts are used to determine which type of contributor (silver, gold, etc.) the user is.
            goldBadgeCount: 0,
            silverBadgeCount: 0,
            // Default paths to badges 
            acceptedEditsBadge: `images/Badges/edits-accepted/bronze.png`,
            apiUsageBadge: `images/Badges/api-usage/bronze.png`,
            communityScoreBadge: `images/Badges/community-score/bronze.png`
        }
    },
    methods: {
        // Gets a single users info. This method is only called when a user is not viewing their own profile.
        async GetUserInfo(){
            let headers = {};
            if (this.$store.getters.loggedIn) {
              headers.Authorization = this.$store.getters.authToken;
            }
            await axios.get(`${constants.API_ENDPOINT}user-one/${this.$route.params.username}`,
                { headers: headers })
                .then(response => {
                    this.ProfileData = response.data;
                    if (this.$store.getters.loggedIn && this.$route.params.username === this.ProfileData.Username){
                        this.$store.commit("changeCurrentUserInfo", response.data);
                    }
                    this.UserInfoLoaded();
                }).catch(() => {
                    let unknownType = 'User';
                    this.$router.push({ name: 'not-found', params: { unknownType }});
                });
        },
        // Gets the Edit or Comment history for a specific user.
        GetUserActivity(activityType) {
            this.gettingUserActivity = true;
            this.activities = [];
            this.FeedActivity = activityType;
            let endpoint = `${constants.API_ENDPOINT}${activityType === 'Edit' ? 'user/edits/' : 'user/comments/'}`;
            let headers = {};
            if (this.$store.getters.loggedIn) {
              headers.Authorization = this.$store.getters.authToken;
            }
            axios.get(endpoint,
                { params: { UserID: this.ProfileData.UserID },
                  headers: headers })
                .then(response => {
                    this.gettingUserActivity = false;
                    this.activities = response.data;
                });
        },
        // Driver which calls getBadge for each type of badge we want to display
        getBadges(){
            this.apiUsageBadge = this.getBadge('api-usage', this.ProfileData['APICalls'], constants.API_USAGE_BADGE_BOUNDARIES);
            this.communityScoreBadge = this.getBadge('community-score', this.ProfileData['CommunityScore'], constants.COMMUNITY_SCORE_BADGE_BOUNDARIES);
            this.acceptedEditsBadge = this.getBadge('edits-accepted', this.ProfileData['AcceptedEdits'], constants.ACCEPTED_EDITS_BADGE_BOUNDARIES);
        },
        // Determines which color of badge should be displayed for the given badge type.
        getBadge(badgeType, badgeScore, badgeBoundaries){
            if (badgeScore >= badgeBoundaries[1]) {
                this.goldBadgeCount++;
                return `images/Badges/${badgeType}/gold.png`;
            } else if (badgeScore >= badgeBoundaries[0]){
                this.silverBadgeCount++;
                return `images/Badges/${badgeType}/silver.png`;
            } else {
                return `images/Badges/${badgeType}/bronze.png`;
            }
        },
        UserInfoLoaded(){
            this.userInfoLoaded = true;
            this.GetUserActivity('Edit');
            this.getBadges();
        }
    },
    mounted: async function() {
        // If a logged in user is accessing their own profile and already has their info loaded, skip API query.
        if (this.$store.getters.currentUserInfo){
            if (this.$store.getters.currentUserInfo.Username === this.$route.params.username){
                this.ProfileData = this.$store.getters.currentUserInfo;
                this.UserInfoLoaded();
            } else {
                await this.GetUserInfo();
            }
        }
        else{
            // If user is not logged in then we need to get the profile data for the viewed user.
            if (!this.$store.getters.loggedIn){
                await this.GetUserInfo();
            }
            // If user is logged in and doesn't have their info yet, the 'watch' block will check to see if
            // they are viewing themselves and update profile info accordingly.
        }
    },
    watch: {
      // If store had to call API to get user info, and the user is viewing themselves, load profile data now.
      '$store.state.currentUserInfo' : async function() {
          let viewingSelf = this.$store.getters.currentUserInfo.Username === this.$route.params.username;
          if (viewingSelf) {
            this.ProfileData = this.$store.getters.currentUserInfo;
            this.UserInfoLoaded();
          }
          else {
            // Not viewing themselves. Get viewed user's data.
            await this.GetUserInfo();
          }
      }
    },
    components: {
    "activity-entry": ActivityEntry
  }

}

</script>

<style scoped>

hr {
    margin-top: 0 0 5px;
}

h3 {
    font-weight: bold;
}

.user-page {
    background-color: #f3f2ef;
}

#user-page-container {
    width: 70%;
    display: flex;
    flex-direction: column;
    margin: 2.5em auto 0;
}

/* 
    User Page Sections
*/

/* All page modules except header section*/
#user-page-container > * {
    margin-top: 20px;
    padding: 2em 4em;
    border-radius: 10px;
    border: 1px solid lightgray;
    background-color: white;
    align-items: center;
}

#user-header {
    margin-top: 0;
    padding: 0 0 1.5em;
}

#user-about p {
    font-size: 1.2rem;
}

#user-feed {
    margin-bottom: 3em;
}

#user-feed-button-container {
    margin-bottom: 1em;
}

/* 
    Header Image and Badges
*/

#banner-image {
    margin-bottom: -80px;
    width: 100%;
    height: 200px;
    border-radius: 10px 10px 0 0;
    object-fit: cover;
}

#badges-container {
    position: relative;
}

.badges {
    position: absolute;
    bottom: 0;
    right: 0;
    margin: 0 10px -80px 0;
}

.badge {
    width: 6em;
    display: inline-block !important;
}

/* 
    Header Content
*/

#header-content {
    display: flex;
    justify-content: space-between;
}

#user-image {
    border-radius: 12em;
    border: 1.5px solid lightgray;
    height: 12em;
    width: 12em;
    object-fit: cover;
    margin: 0 0 -80px 50px;
}

/* 
    Header Content Left
*/

#header-content-left {
    flex: 0.5;
    margin-left: 280px;
}

#user-work-section {
    display: flex;
    flex-wrap: wrap;
}

.contact-info-button {
    min-width: 100px;
    margin-bottom: 0.5em;
    height: 100%;
}

/* User stats section (in header) */

.user-stats-container {
    display: grid;
    grid-auto-columns: 47.5% 5% 47.5%;
    grid-auto-rows: 47.5% 5% 47.5%;
}

.user-stats-container > h6:first-child {
    margin-right: 2em;
}

#user-stat-edits-accepted {
    grid-column: 3;
    grid-row: 1;
}

#user-stat-api-usage {
    grid-column: 3;
    grid-row: 3;
}

#user-stat-community-score {
    grid-column: 1;
    grid-row: 3;
}

#user-stat-edits-submitted {
    grid-column: 1;
    grid-row: 1;
}

/* 
    Header Content Right
*/

#header-content-right {
    flex: 0.3;
}

#header-buttons-right {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    margin-right: 3em;
}

#header-buttons-right > button:first-child {
    margin-right: 1em;
    margin-bottom: 0;
}

.button {
    min-width: 130px;
    border: none;
    background-color: #ff8c00 !important;
}

.btn-outline-primary {
    color: #ff8c00 !important;
    border-color: #ff8c00 !important;
}

.btn-outline-primary:hover {
    color: white !important;
    background-color: #ff8c00 !important;
}

/* 
    Utility classes
*/

.gold {
    color: #FFB302;
}

.silver {
    color: #848482;
}

.bronze {
    color: #CD7F32;
}

.alternative-text {
    color: gray;
    font-size: 1.2rem;
}

@media (max-width: 1200px){
    #user-page-container {
        width: 90%;
    }
}

@media (max-width: 1000px){

    #user-page-container > * + * {
        padding: 1em 2em;
    }

    #banner-image {
        height: 250px;
        margin-bottom: -120px;
    }

    #badges-container {
        display: none;
    }

    #user-image {
        height: 14em;
        width: 14em;
        border-radius: 14em;
        display: block;
        margin: 0 auto 2em;
    }

    #header-content {
        flex-direction: column;
    }

    #header-content-left {
        margin-left: 2em;
    }

    #user-about p {
        font-size: 1rem;
    }

    .section-header, .alternative-text {
        text-align: center;
    }

    #user-feed-button-container {
        display: block;
        margin: 0 auto 1em;
        text-align: center;
    }

    #header-content-left, #header-content-right {
        max-width: 80%;
        min-width: 80%;
        margin: 0 auto;
    }

    #header-buttons-right {
        justify-content: flex-start;
        margin: 1.5em 0 0;
    }
}

@media (max-width: 600px){
    h3 {
        font-size: 1.6rem;
    }

    h4 {
        font-size: 1.2rem;
    }

    #user-image {
        height: 10em;
        width: 10em;
        border-radius: 10em;
        display: block;
        margin: 0 auto 2em;
    }

    #banner-image {
        height: 200px;
        margin-bottom: -100px;
    }

    #header-buttons-right {
        justify-content: center;
    }
}

</style>