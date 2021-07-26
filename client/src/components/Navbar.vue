<template>
  <b-navbar toggleable="lg" id='navbar'>
    <router-link :to="{ name: 'ahj-search' }">
      <b-navbar-brand>
        <img id="oblogo" src="@/assets/ob.png" />
        <h1 class="app-title">AHJ Registry</h1>
      </b-navbar-brand>
    </router-link>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav class="mr-auto navbar-background">
        <!-- show links around the site -->
        <b-nav-item href="#/about">About</b-nav-item>
        <b-nav-item href="#/ahj-search">Search</b-nav-item>
        <b-nav-item href="#/data-vis">Coverage</b-nav-item>
        <b-nav-item href="#/ahj-search/?tutorial=1">Tutorial</b-nav-item>
        <b-nav-item :href="DocumentationLink" target="_blank">Documentation</b-nav-item>
        <b-nav-item v-b-modal.my-modal @click='ResetFeedbackForm'>Help</b-nav-item>
        <feedback-form ref="feedbackFormComponent"></feedback-form>
      </b-navbar-nav>
      <b-navbar-nav class="ml-auto navbar-background">
        <!-- if logged in show pfp, else show login button -->
        <b-nav-item href="#/login" v-if="!loggedIn">Login</b-nav-item>
        <b-nav-item href="#/register" v-if="!loggedIn">Register</b-nav-item>
        <b-nav-item-dropdown right v-if="loggedIn">
            <template #button-content>
              <div class="format"> 
                <img class="user-photo" src="../assets/images/profile-image-default.jpeg">
              </div>
            </template>
            <b-dropdown-item class='dropdown-item' :href="'#/user/' + Username"> 
              <b-icon class='icon' icon="person"></b-icon>
              Profile
            </b-dropdown-item>
            <b-dropdown-item class='dropdown-item' href="#/progress">
            <!-- go to progress page -->
              <b-icon class='icon' icon="bar-chart-line"></b-icon>
              My Progress
            </b-dropdown-item>
            <b-dropdown-item class='dropdown-item' href="#/settings">
            <!-- account setting page -->
              <b-icon class='icon' icon="gear"></b-icon>
              Account Settings
            </b-dropdown-item>
            <b-dropdown-item class='dropdown-item' href="#/logout">
            <!-- Logout -->
            <b-icon class='icon' icon="box-arrow-right"></b-icon>
              Sign Out
            </b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script>
import FeedbackForm from "../components/FeedbackForm.vue";
import constants from "../constants";
export default {
  model: {
    event: 'event-open-modal'
  },
  computed: {
    loggedIn() {
      return this.$store.getters.loggedIn;
    },
    Photo() {
      return this.$store.getters.currentUserInfo ? this.$store.getters.currentUserInfo.Photo : "";
    },
    Username() {
      return this.$store.getters.currentUserInfo ? this.$store.getters.currentUserInfo.Username : "";
    },
    DocumentationLink() {
      return constants.DOCS_ENDPOINT;
    }
  },
  methods: {
    ResetFeedbackForm(){
      this.$refs.feedbackFormComponent.ResetModal();
    }
  },
  components: {
    "feedback-form": FeedbackForm,
  },
}
</script>

<style scoped>

nav {
  font-size: 18px;
  font-style: normal;
  display: flex;
  padding-left: 20px;
  border-bottom: 1px solid #dadce0;
  padding-top: 12px;
}

.navbar-brand {
  margin-right: 30px;
}

#oblogo {
  margin-top: -8px;

  width: auto;
  height: 50px;
}

.nav-link {
  color: #3b3932 !important;
}

.app-title {
  font-family: "Roboto";
  font-size: 25px;
  font-weight: bold;
  display: inline;
  text-transform: uppercase;
  margin-left: 5px;
}

.icon {
  margin-right: 0.2em;
}

.dropdown-item {
  padding-left: 0.5em !important;
}

.user-photo {
  height: 90%;
  object-fit: cover;
  border-radius: 2rem;
}

#nav-collapse {
  z-index: 1040;
}

@media (min-width: 1800px){
  * {
    font-size: 1.3rem;
  }
  nav {
    font-size: 1.3rem;
  }
}

@media (max-width: 990px){
    .navbar-background {
      background-color: rgba(255, 255, 255, 0.9);
  }
}

.dot {
  height: 10px;
  width: 10px;
  background-color: red;
  border-radius: 50%;
  display: inline-block;
  position: absolute;
  left: 75%;
  top: 5px;
  z-index: 5000;
}
h3{
  position: relative;
  font-size: 10px;
  left:20%;
  top:-1px;
  color: white;
  font-family: "Roboto Condensed";
}
.format{
  width: 3em;
  height: 3em;
  object-fit: cover;
  float: left;
  position: relative;
}
</style>