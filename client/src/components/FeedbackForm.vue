<template>
    <b-modal id="my-modal" size="lg" centered scrollable footer-class='modal-footer-custom'>
        <template #modal-title>
            <h1 class='modal-title'>{{`AHJ Registry Feedback Form`}}</h1>
        </template>
        <b-overlay :show="SubmitStatus == 'PENDING'" opacity="0.6">
        <div v-if='SubmitStatus != `SUCCESS`'>
            <h4 class='feedback-form-top-text'>Have some feedback for us or need some help?</h4>
            <h4 class='feedback-form-bottom-text'>Email our team at support@sunspec.org or use the form below.</h4>
            <div class='feedback-body'>
            <div class='form-spacing'>
                <label class="form-label">Email</label>
                <b-form-input size="lg" class="form-input" placeholder="Email" v-model="Email" required :state="$v.Email.$dirty ? !$v.Email.$error : null" alt="Email"></b-form-input>
                <div v-if="$v.Email.$dirty">
                <div class="error" v-if="!$v.Email.required">Email is required.</div>
                <div class="error" v-if="!$v.Email.ValidEmail && Email !== ''">Incorrect email format. Ex: example@example.com</div>
                </div>
            </div>
            <div class='form-spacing'>
                <label class="form-label">Subject</label>
                <b-form-input size="lg" class="form-input" placeholder="Subject" v-model="Subject" required :state="$v.Subject.$dirty ? !$v.Subject.$error : null" alt="Subject"></b-form-input>
                <div v-if="$v.Subject.$dirty">
                <div class="error" v-if="!$v.Subject.required">Subject is required.</div>
                </div>
            </div>
            <div class='form-spacing'>
                <label class="form-label">Message</label>
                <b-form-textarea size="lg" rows="4" class="form-input" placeholder="Message" v-model="Message" required :state="$v.Message.$dirty ? !$v.Message.$error : null" alt="Message"></b-form-textarea>
                <div v-if="$v.Message.$dirty">
                <div class="error" v-if="!$v.Message.required">Message is required.</div>
                </div>
            </div>
            <h4 class='error' v-if='SubmitStatus == `ERROR`'>Something went wrong with sending your email.</h4>
            </div>  
        </div>
        <div v-else>
            <div id="confirmation-title">
                Message sent.
            </div>

            <div id="icon-container">
                <b-icon class="envelope-icon" icon="envelope" font-scale="7.5"></b-icon>
            </div>
            <div id="confirmation-text">
                We'll review your message shortly. Thank you. 
            </div>
        </div>

        </b-overlay>
        <template #modal-footer>
            <b-button size="sm" variant="orange" id='feedback-button' v-bind:class="{ invisible: SubmitStatus == 'SUCCESS' }" :disabled='SubmitStatus==`PENDING`' pill @click="SendMessage">
            Send Message
            </b-button>
        </template>
    </b-modal>
</template>

<script>
import axios from "axios";
import constants from "../constants.js";
import { required } from 'vuelidate/lib/validators';
const ValidEmail = constants.VALID_EMAIL;
export default {
    data() {
      return {
          Email: "",
          Subject: "",
          Message: "",
          SubmitStatus: '',
      }
  },
    methods: {
    ResetModal(){
      this.Email = ''
      this.Subject = ''
      this.Message = ''
      this.SubmitStatus = ''
      this.$v.$reset()
    },
    SendMessage(){
      this.$v.$touch();
      if (!this.$v.$invalid) {
        let that = this;
        this.SubmitStatus = 'PENDING';
        axios.post(`${constants.API_ENDPOINT}contact/`, {
            Email: this.Email,
            Subject: this.Subject,
            Message: this.Message
        }).then(() => {
            that.SubmitStatus = 'SUCCESS';
        })
        .catch(() => {
          this.SubmitStatus = 'ERROR';
        });
      }
    }
  },
  validations: {
        Email: {
            required,
            ValidEmail
        },
        Subject: {
            required
        },
        Message: {
            required
        },
  },
}
</script>

<style scoped>
.error {
  color: red;
  text-align: center;
}
.invisible {
  display: none;
}
.modal-body {
  padding: 3rem !important;
}
.modal-title {
  font-size: 1.8rem !important;
}
.modal-header {
  align-items: center !important;
}
.feedback-body {
  padding: 0.5em 2em;
}
#feedback-button {
  font-size: 1.2rem;
  font-weight: bold;
  color: white;
  width: 30%;
  line-height: 2rem;
  background-color: #ff8c00 !important;
  box-shadow: 1px 3px 2px #888888
}
.feedback-form-top-text {
  text-align: center;
  margin-top: 0.5em;
  font-size: 1.4rem;
}
.feedback-form-bottom-text {
  text-align: center;
  font-size: 1rem;
}
#my-modal___BV_modal_footer_ > *{
  justify-content: center !important;
  margin: auto;
}
.form-label {
  font-size: 1.2rem;
}
.form-spacing {
  margin-bottom: 0.8em;
}
#icon-container {
    margin-top: 2.5rem;
    margin-bottom: 2.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    animation-name: mailSent;
    animation-duration: 1.8s;
    animation-iteration-count: 1;
    animation-timing-function: ease-out;
}
#confirmation-text {
  text-align: center;
  font-size: 1.3rem;
}
#confirmation-title {
  text-align: center;
  font-size: 2.2rem;
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
</style> 
