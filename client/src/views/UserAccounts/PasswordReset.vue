<template>
  <div id="password-reset-container">
    <b-row align-h="center" align-v="center" class="top-buffer">
        <b-col cols="11" md="8" lg="6" xl="4">
        <div class="shadow px-5 py-3 bg-white rounded" id="password-reset-form-container">
            <form @submit.prevent>
                <div class="vertical-center">
                    <span id="password-reset-form-title">
                        Reset Password
                    </span>
                    <template v-if="!this.emailSent">
                        <div class="form-spacing">
                            <label class="form-label">Email</label>
                            <b-form-input size="lg" class="form-input" type="text" v-model="Email" :state="($v.Email.$dirty && !$v.Email.$pending) ? !$v.Email.$error : null" placeholder="Email" alt="Email" value="john@gmail.com"></b-form-input>
                        </div>
                        <div v-if="$v.Email.$dirty">
                            <div class="error" v-if="!$v.Email.required">Email is required.</div>
                            <div class="error" v-if="!$v.Email.ValidEmail && Email !== ''">Incorrect email format. Ex: example@example.com</div>
                        </div>
                        <b-button id="password-reset-button" block pill variant="blue" @click="SendResetRequest">
                            Send password reset email
                        </b-button>
                    </template>
                    <template v-else>
                        <div id="icon-container">
                            <b-icon class="envelope-icon" icon="envelope" font-scale="7.5"></b-icon>
                        </div>
                        <div id="confirmation-text">
                            A password reset link has been sent to {{this.Email}}. 
                        </div>
                    </template>
                </div>
            </form>
        </div>
        </b-col>
    </b-row>
  </div>
</template>

<script>
import axios from "axios";
import constants from "../../constants.js";
import { required } from 'vuelidate/lib/validators';

// Checks if inputted email is valid
const ValidEmail = (email) => /[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*[.][a-zA-Z]+/g.test(email)

export default {
    data() {
        return {
                Email: "",
                emailSent: false
        }
    },
    methods: {
        // If email is correctly formatted, send a message to that email with a password reset link. 
        SendResetRequest() {
            this.$v.$touch();
            if (!this.$v.$invalid) {
                axios.post(constants.API_ENDPOINT + "auth/users/reset_password/", {
                    "Email": this.Email,
                }).then(() => {
                    this.emailSent = true;
                }).catch(() => {
                    alert("Error with resetting password. Inputted email likely not in database.");
                })
            }
        },
    },
    validations: {
        Email: {
            required,
            ValidEmail
        }
    },
}
</script>

<style scoped>

label {
    margin: 0;
    padding: 0;
}

a {
    color: #277bcd;
    font-size: 1rem;
    font-weight: bold;
    margin: .8em 0em;
}

#password-reset-container {
    background-color: #f7f7f7;
    overflow: hidden;
}

.top-buffer { 
    margin-top: 10%; 
}

.vertical-center{
    overflow: hidden;
}
#router-v{
    overflow: hidden;
}
#password-reset-form-title {
    display: inline-block;
    margin-top: 0.8em;
    margin-bottom: 0.4em;
    color: #6b6b6b;
    font: 2.5rem Helvetica;
}

.form-spacing {
    display: block;
    margin-top: 0.5em;
}

.form-label {
    font-size: 1.3rem;
}

.form-input {
    padding: 1em .8em;
    border: 0.5px solid #c0c1c2;
    line-height: 10;
    font: 1.3rem Helvetica;
}

#password-reset-button {
    font-size: 1.3rem;
    font-weight: bold;
    min-width: 220px;
    width: 80%;
    color: white;
    margin: 1.5em auto 0em;
    background-color: #ff8c00 !important;
}

.error {
    color: red;
}

#confirmation-text {
    display: inline-block;
    margin-top: 1.2em;
    font: 1.3rem Helvetica;
    text-align: center;
}

/* Envelope Transition css */
.icon-container {
    margin-top: 1.5em;
    display: flex;
    align-items: center;
    justify-content: center;
}

.envelope-icon {
    transition: all 4s ease-out;
}

.stateOne {
    opacity: 1;
    transform: scale(1, 1);
}

.stateTwo {
    opacity: .5;
    transform: scale(1.9, 1.9);
}

#icon-container {
    margin-top: 1.5em;
    display: flex;
    align-items: center;
    justify-content: center;
    animation-name: mailSent;
    animation-duration: 1.8s;
    animation-iteration-count: 1;
    animation-timing-function: ease-out;
}

@keyframes mailSent {
    0% {
        transform: rotate(0deg);
        opacity: 0;
    }
    50% {
        transform: rotate(360deg);
        opacity: 1;
    }
    65% {
        transform: scale(1.3);
    }
    100% {
        transform: scale(1);
    }
}

@media (max-width: 650px){
    #password-reset-button {
        font-size: 1rem;
    }
}

</style>
