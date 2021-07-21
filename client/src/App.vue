<template>
  <div id="app">
    <Navbar id="navbar" />
    <b-modal v-model="showAPIErrorInfo" ok-only>
      <template #modal-title>Notification</template>
      <span v-if="apiErrorInfo.status === 429" v-html="constants.API_THROTTLE_MSG" />
      <span v-else>
        An error with loading the data has occurred. Please try again.
      </span>
    </b-modal>
    <router-view id="router-v" />
  </div>
</template>

<script>
import Navbar from "./components/Navbar.vue";
import constants from "@/constants";

export default {
  data() {
    return {
      showAPIErrorInfo: false
    }
  },
  computed: {
    apiErrorInfo() {
      return this.$store.state.apiErrorInfo;
    },
    constants() {
      return constants;
    }
  },
  watch: {
    '$store.state.apiErrorInfo': function (newVal) {
      if (newVal.status) {
        this.showAPIErrorInfo = true;
      }
    }
  },
  components: {
    Navbar,
  },
  mounted() {
    this.$store.commit('resetAPIErrorInfo');
    if (this.$store.getters.loggedIn) {
      this.$store.dispatch('getUserInfo')
    }
  },
};
</script>

<style>
#app {
  font-family: "Roboto Condensed";

  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  background-color: white;
  display: grid;
  grid-template-rows: 4.25em auto;
  height: 100vh;
}

#navbar {
  grid-row: 1 / 2;
}
</style>
