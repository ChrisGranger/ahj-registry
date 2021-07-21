<template>
    <div class="edit-profile-container">
        <h1 class="setting-title">Edit Profile</h1>
        <template v-if="this.profileInfoLoaded">
            <div class="header">
                <img class="user-photo" src="../../../assets/images/profile-image-default.jpeg">
                <div class="header-user-identifiers" v-if="formFirstNameCapital !== ''">
                    <h2>{{`${formFirstNameCapital} ${formLastNameCapital}`}} </h2>
                </div>
                <div v-else>
                    <h2><b>{{Username}}</b></h2>
                </div>
            </div>
            <form @submit.prevent id="registration-form">

                <div class="form-spacing">
                    <label>Name</label>
                    <div class="flex-row">
                        <b-form-input size="lg" class="form__input" type="text" placeholder="First Name" :state="$v.formFirstNameCapital.$dirty ? !$v.formFirstNameCapital.$error : null" required v-model="formFirstNameCapital" alt="First Name"></b-form-input>
                        <b-form-input size="lg" class="form__input" type="text" placeholder="Last Name" :state="$v.formLastNameCapital.$dirty ? !$v.formLastNameCapital.$error : null" required v-model="formLastNameCapital" alt="Last Name"></b-form-input>
                    </div>
                </div>
                <!-- If the validation object ($v) has been touched, check to see if the form satisfies the validators (in this case, first and last are only required)-->
                <div v-if="$v.$dirty">
                    <div class="error" v-if="!$v.formFirstNameCapital.required || !$v.formLastNameCapital.required">First and Last name are required.</div>
                </div>
                <div class="form-spacing">
                    <label class="form-label">Username</label>
                    <div class='spinner-row'>
                        <b-spinner class="spinner" variant="secondary" v-if="usernameCheckPending"></b-spinner>
                        <b-form-input size="lg" class="form-input" type="text" placeholder="Username" required v-model="FormUsername" v-on:input="CheckUsernameUnique" :state="($v.FormUsername.$dirty && !usernameCheckPending) ? usernameIsUnique && !$v.FormUsername.$error : null" alt="Username"></b-form-input>
                    </div>
                </div>
                <div v-if="$v.FormUsername.$dirty">
                    <div class="error" v-if="!$v.FormUsername.required">Username is required.</div>
                    <div class="error" v-if="!this.usernameIsUnique && !this.usernameCheckPending">Username is already taken.</div> 
                </div>
                <div class="form-spacing">
                    <label>Work Phone</label>
                    <b-form-input size="lg" class="form__input" type="text" placeholder="Work Phone" :state="$v.WorkPhone.$dirty ? !$v.WorkPhone.$error : null" v-model="WorkPhone" alt="Work Phone"></b-form-input>
                </div>
                <!-- Same as above validator, except this time it checks the format of the phone. This was a custom validator written.-->
                <div v-if="$v.$dirty">
                    <div class="error" v-if="!$v.WorkPhone.PhoneFormat">Incorrect Phone Format. Recommended format: 123-456-7890</div>
                </div>
                <div v-else>
                    <b-form-text id="phone-help-text">Recommended phone format: 123-456-7890</b-form-text>
                </div>
                <div class="form-spacing">
                    <label>Preferred Contact Method</label>
                    <b-form-select v-model="userInfo.PreferredContactMethod" class="search-input" :options="['Email', 'WorkPhone']" />
                </div>
                <div class="form-spacing">
                    <label>Bio</label>
                    <b-form-textarea id="textarea-default" size="sm" rows="3" placeholder="Bio" v-model="userInfo.PersonalBio" alt="Bio"></b-form-textarea>
                </div>
                <div class="form-spacing">
                    <label>URL</label>
                    <b-form-input size="lg" class="form__input" type="text" placeholder="URL" required v-model="userInfo.URL" alt="URL"></b-form-input>
                </div>
                <div class="form-spacing">
                    <label>Job Title</label>
                    <b-form-input size="lg" class="form__input" type="text" placeholder="Job Title" required v-model="userInfo.Title" alt="Job Title"></b-form-input>
                </div>
                <div class="form-spacing">
                    <label>Company Affiliation</label>
                    <b-form-input size="lg" class="form__input" type="text" placeholder="Company Affiliation" required v-model="userInfo.CompanyAffiliation" alt="CompanyAffiliation"></b-form-input>
                </div>
                <b-button id="edit-profile-button" @click="UpdateDatabase" :disabled="this.SubmitStatus === 'PENDING' || usernameCheckPending || !this.usernameIsUnique" block pill variant="primary">
                    Update Profile
                </b-button>
                <h4 class="api-status-text" v-if="this.SubmitStatus === 'PENDING'"> Updating profile... </h4>
                <h4 class="api-status-text success" v-if="this.SubmitStatus === 'OK'"> Your profile information has been updated! </h4>
                <h4 class="api-status-text error" v-if="this.SubmitStatus === 'ERROR'"> Something went wrong with updating your information. </h4>
            </form>
        </template>
        <template v-else>
            <p>Loading...</p>
        </template>
    </div>
</template>

<script>
import axios from "axios";
import constants from "../../../constants.js";
import { required, helpers } from 'vuelidate/lib/validators';

// Enforce phone format but also evaluate to true if empty string (not a required field)
let PhoneFormat = (value) => !helpers.req(value) || constants.VALID_PHONE(value);
export default {
    computed: {
        // Getters and setters to always give the first name and last name inputs a capital letter
        formFirstNameCapital: {
            get: function () {
                    return this.userInfo.FirstName;
                },
            set: function (newFirstName) {
                if(newFirstName.length < 1) {this.userInfo.FirstName = ''; return}
                this.userInfo.FirstName = this.CapitalizeFirstLetter(newFirstName);
            }
        },
        formLastNameCapital: {
            get: function () {
                    return this.userInfo.LastName;
                },
            set: function (newLastName) {
                if(newLastName.length < 1) {this.userInfo.LastName = ''; return}
                this.userInfo.LastName = this.CapitalizeFirstLetter(newLastName);
            }
        },
        FormUsername: {
            get: function () {
                    return this.userInfo.Username;
                },
            set: function (newUsername) {
                this.userInfo.Username = newUsername;
            }
        },
        WorkPhone: {
            get: function() {
                return this.userInfo.WorkPhone;
            },
            set: function (newWorkPhone) {
                this.userInfo.WorkPhone = newWorkPhone;
            }
        },
        UserData() {
            return this.$store.getters.currentUserInfo;
        },
    },
    data() {
        return {
            // UserInfo object that corresponds to values on a typical user object
            userInfo: {
                FirstName: null,
                LastName: null,
                PersonalBio: null,
                URL: null,
                Title: null,
                CompanyAffiliation: null,
                WorkPhone: null,
                PreferredContactMethod: null,
                Username: null,
            },
            OriginalUsername: null,
            Photo: '../../../assets/images/profile-image-default.jpeg',
            SubmitStatus: '',
            profileInfoLoaded: false,
            usernameIsUnique: true,
            usernameCheckPending: false
        }
    },
    methods: {
        // When we retrieve the logged in user's info when page loaded, update the values of the form's fields.
        UpdateComponentData(StoreProfileData) {
            if (StoreProfileData !== null){
                let that = this;
                // All fields are either on the surface level user object or within the Contact object (accessed by COntactID)
                // Iterate through all and update our locally stored userInfo variable.
                Object.keys(that.userInfo).map(function(key) {
                    if (StoreProfileData[key])
                        that.userInfo[key] = StoreProfileData[key];
                    else if (StoreProfileData['ContactID'][key])
                        that.userInfo[key] = StoreProfileData['ContactID'][key].Value;
                });
                this.userInfo.FirstName = StoreProfileData.ContactID['FirstName'].Value;
                this.userInfo.LastName = StoreProfileData.ContactID['LastName'].Value;
                this.userInfo.URL = StoreProfileData.ContactID['URL'].Value;
                this.userInfo.Title = StoreProfileData.ContactID['Title'].Value;
                this.userInfo.WorkPhone = StoreProfileData.ContactID['WorkPhone'].Value;
                this.userInfo.PreferredContactMethod = StoreProfileData.ContactID['PreferredContactMethod'].Value;
                this.Username = StoreProfileData['Username'];
                this.OriginalUsername = StoreProfileData['Username'];
            }
        },
        // Query the database with the new data inputted into the form.
        UpdateDatabase(){
            // We don't want to mark fields as incorrect until the user has tried each one. Touching the $v object will
            // make it so that if any validations fail, then we now mark those fields as incorrect.
            this.$v.$touch();
            // only proceed if all validations passed
            if (!this.$v.$invalid && !this.usernameCheckPending && this.usernameIsUnique) {
                this.SubmitStatus = "PENDING";
                // Only reformat workphone if there is any input
                if (this.userInfo.WorkPhone)
                    this.userInfo.WorkPhone = this.FormatPhone(this.userInfo.WorkPhone);

                // Put all data we want to send to the server into a FormData object
                let fd = new FormData();
                for (let userAttr in this.userInfo){
                    // If the user attribute is non-empty, add to FormData object
                    if (this.userInfo[userAttr])
                        fd.append(`${userAttr}`, this.userInfo[userAttr]);
                }
                axios.post(`${constants.API_ENDPOINT}user/update/`, fd,
                    { headers: { 'Content-Type': 'multipart/form-data',
                                 Authorization:  this.$store.getters.authToken }})
                .then(() => { 
                    this.SubmitStatus = "OK"; 
                    this.UpdateStore(fd);
                })
                .catch(() => { this.SubmitStatus = "ERROR"; });
            }
        },
        // Update the store's currentUserInfo variable with the new values
        UpdateStore(fd){
            let currUserInfo = this.$store.state.currentUserInfo;
            for (let key in fd.keys()){
                if (currUserInfo[key])
                    currUserInfo[key] = fd.get(key);
                else if (currUserInfo['ContactID'][key])
                    currUserInfo['ContactID'][key] = fd.get(key);
            }
            if (fd.has('Photo'))
                currUserInfo.Photo = URL.createObjectURL(fd.get('Photo'));
        },
        CapitalizeFirstLetter(string) {
            return string.charAt(0).toUpperCase() + string.slice(1);
        },
        FormatPhone(phone){
            phone = phone.replaceAll('-',"");
            phone = phone.replaceAll('(',"");
            phone = phone.replaceAll(')',"");
            return `(${phone.slice(0,3)})${phone.slice(3,6)}-${phone.slice(6,10)}`
        },
        UpdatePhoto() {
            let url = URL.createObjectURL(document.getElementById("image-picker").files[0]);
            this.Photo = url;
        },
        async CheckUsernameAvailable(){
            axios.get(constants.API_ENDPOINT + "auth/form-validator/",
                { params: { Username: this.userInfo.Username },
                  headers: { Authorization: this.$store.getters.authToken }})
                .then(response => {
                    if (this.usernameCheckPending){
                        this.usernameCheckPending = false;

                        if (this.userInfo.Username !== this.OriginalUsername){
                            this.usernameIsUnique = !response.data.UsernameExists;
                        }
                        else {
                            this.usernameIsUnique = true;
                        }
                        this.$v.FormUsername.$touch();
                    }
                }).catch(() => {return 'BACKEND ERROR'});
        },
        CheckUsernameUnique(){
            this.usernameCheckPending = true;
            clearTimeout(this.usernameTimer);
            this.usernameTimer = setTimeout(this.CheckUsernameAvailable, 1000);
        },
    },
  mounted() {
    // Get user's info if the store isn't already currently fetching it (which happens on app reload). 
    if (this.$store.getters.currentUserInfo)
        this.$store.dispatch('getUserInfo');
  },
  watch: {
      // If store had to call API to get user info, update this component's data when API request is finished.
      '$store.state.currentUserInfo' : function(newval) {
        this.UpdateComponentData(newval);
        this.profileInfoLoaded = true;
      }
  },
  // validations that must be passed for the corresponding field
  validations: {
        formFirstNameCapital: {
            required
        },
        formLastNameCapital: {
            required
        },
        FormUsername: {
            required,
        },
        WorkPhone: {
            PhoneFormat
        }
  },
}
</script>

<style scoped>

.setting-title {
    margin-bottom: 0.5em;
}

label {
    font-size: 18px;
    font-weight: 800;
}

.flex-row {
    flex: 100%;
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
}

#textarea-default {
    font-size: 1.2rem;
}

.form-spacing {
    margin: 20px auto;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.form-spacing > label {
    flex: 30%;
}
.form-spacing.form__input {
    flex: 70%;
    margin-left: 1em;
}

.flex-row > * {
    width: 48%;
}
.flex-row > label {
    flex: 10%;
    align-items: center;
    vertical-align: center;
    text-align: left;
}

.user-photo {
  width: 8em;
  height: 8em;
  border-radius: 8em;
  margin-right: 1em;
  object-fit: cover;
}

#edit-profile-button{
    border: none;
    background-color: #ff8c00 !important;
}

.header {
    display: flex;
    margin: 1em;
}

.header-user-identifiers > *{
    margin: 10px;
    padding: 0.5em 0px;
}

.api-status-text {
    text-align: center;
    margin-top: 20px;
}

.error {
    color: red;
}

.success {
    color: green;
}

#phone-help-text {
    font-size: 1rem;
}

#image-picker {
    margin-left: 0.5em;
}

.spinner {
    position: absolute;
    left: 95%;
    top: 14px;
    width: 1.5em; 
    height: 1.5em;
}

.spinner-row {
    position: relative;
}

@media (max-width: 1300px){
    .spinner {
        left: 92%;
    }
}

@media (max-width: 650px){
    .user-photo {
        width: 6em;
        height: 6em;
        border-radius: 6em;
        margin-right: 1em;
    }
    .header-user-identifiers h2{
        margin: 5px;
        font-size: 1.5rem;
    }
    .form-spacing {
        flex-direction: column;
    }
    #textarea-default {
        font-size: 1rem;
    }
}

</style>