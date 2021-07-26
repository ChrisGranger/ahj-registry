<template>
    <div>
        <h1>API</h1>
        <div>
            <h4 id="api-description-text">
                Our API allows searching AHJs by:
                <ul>
                  <li v-for="x in APIFilters" :key="x">{{ x }}</li>
                </ul>
                <b-button id="documentation-button" class="button" disabled block pill variant="primary">
                    Go to Documentation
                </b-button>
                To use the API, please contact <span v-html="getMembershipMailTo()" /> to activate your API token.
            </h4>
            <b-table :fields="fields" :items="items" outlined :busy="!this.items.length">
                <template #table-busy>
                    <div class="text-center text-primary my-2">
                        <b-spinner class="align-middle"></b-spinner>
                        <strong>&nbsp; Loading...</strong>
                    </div>
                </template>
                <template #cell(auth_token)="data">
                  Token {{ data.item.auth_token }}
                </template>
                <template #cell(is_active)="data">
                  {{ data.item.is_active ? 'Yes' : 'No' }}
                </template>
                <template #cell(expires)="data">
                  {{ data.item['expires'] ? formatDate(data.item.expires) : '---' }}
                </template>
            </b-table>
        </div>
    </div>
</template>

<script>
import moment from "moment";
import constants from "../../../constants";

export default {
    mounted() {
        if (!this.$store.getters.currentUserInfo) {
           this.$store.dispatch('getUserInfo');
        }
    },
    data() {
        return {
            APIFilters: ['Address', 'Location', 'AHJ ID', 'Building Codes', 'And More']
        }
    },
    computed: {
      fields() {
          return this.items.length ? Object.keys(this.items[0]) : [];
      },
      items() {
          let userInfo = this.$store.getters.currentUserInfo;
          return userInfo ? [userInfo.APIToken] : [];
      }
    },
    methods: {
        formatDate(date) {
            return moment(date).format('MMMM Do YYYY, h:mm:ss a');
        },
        getMembershipMailTo() {
            return `<a href="mailto:${constants.MEMBERSHIP_EMAIL}">${constants.MEMBERSHIP_EMAIL}</a>`

        }
    }
}
</script>

<style scoped>
h1 {
    margin-bottom: 0.5em;
}
.button {
    width: 30%;
    min-width: 180px;
    border: none;
    background-color: #ff8c00 !important;
}
#documentation-button {
    margin-bottom: 25px;
}
#generate-token-button {
    margin-bottom: 5px;
}
#api-description-text {
    margin-bottom: 1.5em;
}
#get-token-button{
    margin-bottom: 25px;
}
.api-status-text {
    margin-top: 30px;
}
.error{
    color: red;
}
@media (max-width: 1000px){
    #api-description-text {
        font-size: 1.2rem;
    }
}
@media (max-width: 650px){
    h1 {
        font-size: 2.2rem;
    }
    .api-status-text {
        font-size: 1rem;
    }
    #api-token-text span {
        font-size: .9rem;
    }
}
</style>