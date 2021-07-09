<template>
    <div>
        <h1>API</h1>
        <div>
            <h4 id="api-description-text">Our API makes searching and filtering AHJs by location, AHJ ID, Building Code type, and many other attributes an easy process. 
                Documentation for our API is still in the works. To obtain an API token, contact us at support@sunspec.org.</h4>
            <b-button id="documentation-button" class="button" disabled block pill variant="primary">
                Go to Documentation
            </b-button>
        </div>
        <b-button id="get-token-button" class="button" @click="displayAPIToken" block pill variant="primary">Get Current API Token</b-button>
        <h4 class="api-status-text" v-if="this.showAPIToken">Your current API token: <span>{{this.getCurrentToken()}}</span></h4>
    </div>
</template>

<script>
import axios from "axios";
import constants from "../../../constants.js";
export default {
    data() {
        return {
            APIToken: "",
            generatedAPIToken: false,
            SubmitStatus: "",
            showAPIToken: false
        }
    },
    methods: {
        // Calls the APIToken create method in the backend which destroys the current user api token and returns a new one.
        GenerateAPIToken() {
            this.SubmitStatus = "PENDING";
            this.showAPIToken = false;
            axios.get(constants.API_ENDPOINT + "auth/api-token/create/", 
                        {
                            headers: {
                                Authorization: this.$store.getters.authToken
                            }
                        }
                    )
                    .then((response) => {
                        this.SubmitStatus = "OK";
                        this.APIToken = response.data['auth_token'];
                        this.generatedAPIToken = true;
                        this.$store.state.currentUserInfo.APIToken = response.data['auth_token'];
                    })
                    .catch(() => {
                        this.SubmitStatus = "ERROR";
                    });
        },
        displayAPIToken(){
            this.generatedAPIToken = false;
            if(this.showAPIToken){
                this.showAPIToken = false;
            }
            else{
                this.showAPIToken = true;
            }
        },
        getCurrentToken(){
            if(!this.$store.state.currentUserInfo.APIToken){
                axios.get(constants.API_ENDPOINT + "auth/api-token/create/", 
                        {
                            headers: {
                                Authorization: this.$store.getters.authToken
                            }
                        }
                    )
                    .then((response) => {
                        this.APIToken = response.data['auth_token'];
                        this.generatedAPIToken = true;
                        this.$store.state.currentUserInfo.APIToken = response.data['auth_token'];
                        return this.$store.state.currentUserInfo.APIToken;
                    })
            }
            else{
                return this.$store.state.currentUserInfo.APIToken;
            }
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