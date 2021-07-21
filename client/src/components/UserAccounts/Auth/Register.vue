<template>
  <div id="register-component-container">
    <b-row align-h="center" align-v="center" id="register-component-row">
        <b-col cols="11" md="8" lg="6" xl="4">
        <div class="shadow py-3 bg-white rounded" id="register-form-container">
            <template v-if="submitStatus !== 'OK'">
                <form @submit.prevent id="registration-form">
                    <div class="vertical-center">
                        <h1 id="register-form-title">
                            Sign up
                        </h1>

                        <b-alert v-model="backendErrorOccurred" variant="danger" dismissible> {{errorMessage}} </b-alert>

                        <div class="form-spacing flex-row">
                            <div class="form-name-section">
                                <label class="form-label">First Name</label>
                                <b-form-input size="lg" class="form-input" type="text" placeholder="First Name" required v-model="FirstName" :state="$v.FirstName.$dirty ? !$v.FirstName.$error : null" alt="First Name"></b-form-input>
                            </div>
                            <div class="form-name-section">
                                <label class="form-label">Last Name</label>
                                 <b-form-input size="lg" class="form-input" type="text" placeholder="Last Name" required v-model="LastName" :state="$v.LastName.$dirty ? !$v.LastName.$error : null" alt="Last Name"></b-form-input>
                            </div>
                        </div>
                        <!-- If the user has tried to submit the form (validator object ($v) is dirty) and it does not pass validations for this field, 
            show the corresponding error message -->
                        <div v-if="$v.$dirty">
                            <div class="error" v-if="!$v.FirstName.required || !$v.LastName.required">First and Last name are required.</div>
                        </div>
                        <div class="form-spacing">
                            <label class="form-label">Username</label>
                            <div class='spinner-row'>
                                <b-spinner class="spinner" variant="secondary" v-if="usernameCheckPending"></b-spinner>
                                <b-form-input size="lg" class="form-input" type="text" placeholder="Username" required v-model="Username" v-on:input="CheckUsernameUnique" :state="($v.Username.$dirty && !usernameCheckPending) ? !$v.Username.$error : null" alt="Username"></b-form-input>
                            </div>
                        </div>
                        <div v-if="$v.Username.$dirty">
                            <div class="error" v-if="!$v.Username.required">Username is required.</div>
                            <div class="error" v-if="!this.usernameIsUnique && !this.usernameCheckPending">Username is already taken.</div> 
                        </div>

                        <div class="form-spacing">
                            <label class="form-label">Email</label>
                            <div class='spinner-row'>
                                <b-spinner class="spinner" variant="secondary" v-if="emailCheckPending"></b-spinner>
                                <b-form-input size="lg" class="form-input" type="email" placeholder="Email" required v-model="Email" v-on:input="CheckEmailUnique($event)" :state="($v.Email.$dirty && !emailCheckPending) ? !$v.Email.$error : null" alt="Email"></b-form-input>
                            </div>
                        </div>
                        <div v-if="$v.Email.$dirty">
                            <div class="error" v-if="!$v.Email.required">Email is required.</div>
                            <div class="error" v-if="!$v.Email.ValidEmail && Email !== ''">Incorrect email format. Ex: example@example.com</div>
                            <div class="error" v-if="!this.emailIsUnique && !this.emailCheckPending">Email is already registered.</div>
                        </div>

                        <div class="form-spacing">
                            <label class="form-label">Password</label>
                            <b-form-input size="lg" class="form-input" type="password" placeholder="Password" required v-model="Password" :state="$v.Password.$dirty ? (!$v.Password.$error || (this.backendPasswordError !== null && (this.Password !== this.previousPassword))) : null" alt="Password"></b-form-input>
                        </div>
                        <div v-if="$v.Password.$dirty">
                            <div class="error" v-if="!$v.Password.required">Password is required.</div>
                            <div class="error" v-if="!$v.Password.minLength && Password !== ''">Password must be at least {{ $v.Password.$params.minLength.min }} characters.</div>
                            <div class="error" v-if="(!$v.Password.ContainsNumOrSpecialChar || !$v.Password.ContainsLetter) && Password !== ''">Atleast one letter and one number/symbol.</div>
                            <div class="error" v-if="backendPasswordError && (this.Password === this.previousPassword)">{{backendPasswordError}}</div>
                        </div>
                        <div v-else>
                            <b-form-text id="password-help-text">Must have 8 or more characters with atleast one letter and one number/symbol.</b-form-text>
                        </div>

                        <div class="form-spacing">
                            <label class="form-label">Confirm Password</label>
                            <b-form-input size="lg" type="password" class="form-input" placeholder="Confirm Password" required v-model="ConfirmPassword" :state="$v.ConfirmPassword.$dirty ? (!$v.ConfirmPassword.$error && ConfirmPassword !== '') : null" alt="Confirm Password"></b-form-input>
                        </div>
                        <div v-if="$v.ConfirmPassword.$dirty">
                            <div class="error" v-if="!$v.ConfirmPassword.sameAsPassword">Passwords must be identical.</div>
                        </div>
                        <b-button id="register-button" @click="submitRegistration" :disabled="(this.$v.$invalid && this.$v.$dirty) || (this.submitStatus === 'PENDING') || this.isQueryingDataBase" block pill variant="orange">
                            Sign up
                        </b-button>

                        <h4 class="api-status-text text-center" v-if="this.submitStatus === 'PENDING'"> Creating account... </h4>

                        <div class="text-center">
                            <span> Already have an account? </span>
                            <a href="#/login">
                                Login
                            </a>
                        </div>
                    </div>
                </form>
            </template>
            <template v-else>
                <span id="confirmation-title">
                    Activation email sent!
                </span>

                <div id="icon-container">
                    <b-icon class="envelope-icon" icon="envelope" font-scale="7.5"></b-icon>
                </div>
                <div id="confirmation-text">
                    To activate your account, click on the activation link sent to {{this.Email}}. 
                </div>
            </template>
        </div>
        </b-col>
    </b-row>
    </div>
</template>

<script>
import axios from "axios";
import constants from "../../../constants.js";
import { required, minLength, sameAs } from 'vuelidate/lib/validators';

// Validators we will use for the different form fields. Added as validators for specific fields under the below validations{} section.
const ValidEmail = constants.VALID_EMAIL;
const ContainsNumOrSpecialChar = constants.NUM_OR_SPECIAL_CHAR;
const ContainsLetter = constants.CONTAINS_LETTER;
function EmailNotPending (value){ value; return !this._data.emailCheckPending; }
function EmailUnique (value){ value; return this._data.emailIsUnique; }
function UsernameNotPending (value){ value; return !this._data.usernameNotPending;}
function UsernameUnique (value) { value; return this._data.usernameIsUnique;}

export default {
    data() {
        return {
            Email: "",
            Password: "",
            ConfirmPassword: "",
            FirstName: "",
            LastName: "",
            Username: "",
            submitStatus: null,
            backendPasswordError: null,
            backendErrorOccurred: false,
            errorMessage: "",
            previousPassword: "",

            emailTimer: null,
            emailCheckPending: false,
            emailIsUnique: true,

            usernameTimer: null,
            usernameCheckPending: false,
            usernameIsUnique: true
        }
    },
    computed: {
        isQueryingDataBase() {
            return this.usernameCheckPending || this.emailCheckPending;
        }
    },
    methods: {
         submitRegistration() {
            // Touch the validator object (now making it dirty) so now if any validations fail, the incorrcet fields will show error messages.
            this.$v.$touch();
            // If all validations checks pass, call the api to create the user.
            if (!this.$v.$invalid && !this.isQueryingDataBase) {
                this.submitStatus = 'PENDING';
                this.backendErrorOccurred = false;
                // Create a user with the given email, password, and username fields.
                axios.post(constants.API_ENDPOINT + "auth/users/", {
                    "Email": this.Email,
                    "password": this.Password,
                    "Username": this.Username,
                    "FirstName": this.FirstName,
                    "LastName": this.LastName
                }).then(() => {
                    this.submitStatus = 'OK';
                    document.getElementById("registration-form").reset();
                }).catch(error => {
                    this.submitStatus = 'ERROR';
                    if (error.response){
                        // If password error, display the password error underneath the password field
                        if (error.response.data.password){
                            this.submitStatus = null;
                            this.backendPasswordError = error.response.data.password[0];
                            this.previousPassword = this.Password;
                        }
                    }
                    // If it wasn't a password error, then the problem occured with the backend somehow.
                    else {
                        this.backendErrorOccurred = true;
                        this.errorMessage = "Something went wrong with signing you up.";
                    }
                });
            }
        },
        async CheckUsernameAvailable(){
            axios.get(`${constants.API_ENDPOINT}auth/form-validator/`,
                { params: { Username: this.Username }})
                .then(response => {
                    if (this.usernameCheckPending){
                        this.usernameCheckPending = false;
                        this.usernameIsUnique = !response.data.UsernameExists;
                        this.$v.Username.$touch();
                    }})
                .catch(() => {return 'BACKEND ERROR'});
        },
        async CheckEmailAvailable(){
            axios.get(constants.API_ENDPOINT + "auth/form-validator/",
                { params: { Email: this.Email }})
                .then(response => {
                    if (this.emailCheckPending){
                      this.emailCheckPending = false;
                      this.emailIsUnique = !response.data.EmailExists;
                      this.$v.Email.$touch();
                    }})
                .catch(() => {return 'BACKEND ERROR'});
        },
        CheckUsernameUnique(){
            this.usernameCheckPending = true;
            clearTimeout(this.usernameTimer);
            this.usernameTimer = setTimeout(this.CheckUsernameAvailable, 1000);
        },
        CheckEmailUnique(){
            this.emailCheckPending = true;
            clearTimeout(this.emailTimer);
            this.emailTimer = setTimeout(this.CheckEmailAvailable, 1000);
        },
    },
    mounted() { 
        // If an email was passed in through the route, set the email field to this value.
        if (this.$route.params.email) { 
            this.Email = this.$route.params.email; 
        } 
    },
    validations: {
        LastName: {
            required
        },
        FirstName: {
            required
        },
        Username: {
            required,
            UsernameNotPending,
            UsernameUnique,
        },
        Email: {
            required,
            ValidEmail,
            EmailNotPending,
            EmailUnique,
        },
        Password: {
            required,
            minLength: minLength(8),
            ContainsNumOrSpecialChar,
            ContainsLetter
        },
        ConfirmPassword: {
            sameAsPassword: sameAs('Password')
        }
  }
}
</script>

<style scoped>
label {
    margin: 0;
    padding: 0;
}

a {
    color: #196dd6;
    font-size: 1rem;
    font-weight: bold;
}

#register-form-container {
    margin-bottom: 3em;
    width: 100%;
}

#register-component-row {
    width: 100%;
    margin-top: 3%;
}

#registration-form {
    width: 80%;
    margin: auto;
}

#register-form-title {
    margin-top: 0.8em;
    margin-bottom: 0.2em;
    color: #6b6b6b;
    font: 2.5rem Helvetica;
}

.form-label {
    font-size: 1.3rem;
}

.form-spacing {
    display: block;
    margin-top: 1em;
}

.form-input {
    padding: 1em .8em;
    border: 0.5px solid #c0c1c2;
    line-height: 10;
    font: 1.3rem Helvetica;
}

.form-name-section {
    display: flex;
    flex-direction: column;
}

.flex-row {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
}

.flex-row > * {
    width: 48%;
}

#password-help-text {
    margin-bottom: 1em;
}

#register-button {
    margin: 1em auto;
    font-size: 1.3rem;
    font-weight: bold;
    color: white;
    width: 60%;
    background-color: #ff8c00 !important;
}

.api-status-text {
    text-align: center;
    margin: 1em;
}

.error {
    color: #dc3545;
}

.spinner {
    position: absolute;
    left: 90%;
    top: 14px;
    width: 1.5em; 
    height: 1.5em;
}

.spinner-row {
    position: relative;
}

.b-overlay {
    z-index: -1;
}

.bg-light {
    z-index: -1;
}

#confirmation-title {
    margin: 0.8em 0em 0.2em;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #6b6b6b;
    font: 2.2rem Helvetica;
}

#confirmation-text {
    display: inline-block;
    margin-top: 1.5em;
    font: 1.3rem Helvetica;
    text-align: center;
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

@media (max-width: 500px){
    #registration-form {
        width: 90%;
    }
}

</style>
