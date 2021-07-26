<template>
    <div ref="insp" class="inspection-card">
        <div class="header">
            <!-- show name as header -->
            <h2 v-if="!isEditing">{{this.data.AHJInspectionName !== null && this.data.AHJInspectionName.Value !== "" ? this.data.AHJInspectionName.Value: "No Name"}}
            </h2>
            <h3 class="head" v-else> <input type="text" v-model="Edits.AHJInspectionName"> </h3>
            <div style="display:flex">
            <div style="width: 50px;margin-right:10px;" v-if="eID >= 0">
                <i style="margin-right:10px;margin-top:10px;" v-if="$parent.isManaged && this.editstatus==='P'" v-on:click="$emit('official',{Type:'Accept',eID: eID});editstatus = 'A';changeStatus();" class="fa fa-check"></i>
                <i style="margin-right:5px;" v-if="$parent.isManaged && this.editstatus==='P'" v-on:click="$emit('official',{Type:'Reject',eID: eID});editstatus='R';changeStatus();" class="fa fa-times"></i>
                <i v-if="$parent.isManaged && this.data.ReviewStatus!=='P'" v-on:click="undoStatusChange()" class="fas fa-undo"></i>
            </div>
            <i ref='chev' style="height:100%;margin-right: 10px;margin-top:10px;" class="fa fa-chevron-down" v-on:click="showInfo()"></i>
            <div style="float: right;" v-if="isEditing">
                <!-- button to delete this edit object -->
                <i v-if="!isDeleted" ref='del' style="margin-right: 10px;margin-top:10px;" v-on:click="isDeleted = true" class="fa fa-minus"></i>
                <i v-else v-on:click="isDeleted=false" style="margin-right: 10px;margin-top:10px;" class="fas fa-exclamation-triangle"></i>
            </div>
            </div>
        </div>
        <!-- Inspection info -->
        <div ref="hidden" class="body hide">
        <div style="border-right:1px solid black" class="info-div-insp">
            <div v-if="!this.isEditing">
                <h3> Notes: {{this.data.AHJInspectionNotes !== null && this.data.AHJInspectionNotes.Value !== "" ? this.data.AHJInspectionNotes.Value : "No Notes"}}</h3>
                <h3> Description: {{this.data.Description !== null && this.data.Description.Value !== "" ? this.data.Description.Value : "No Description"}}</h3>
                <h3> FileFolderURL: {{this.data.FileFolderURL !== null && this.data.FileFolderURL.Value !== "" ? this.data.FileFolderURL.Value : "No URL"}}</h3>
                <h3> Type: {{this.data.InspectionType !== null && this.data.InspectionType.Value !== "" ? this.data.InspectionType.Value : "No Type"}}</h3>
                <h3> Technician Required: {{this.data.TechnicianRequired !== null && this.data.TechnicianRequired.Value !== "" ? this.data.TechnicianRequired.Value : "Unknown"}}</h3>
            </div>
            <div v-else>
                <!-- if being edited, display text boxes -->
                <h3> Notes: <input type="text" v-model="Edits.AHJInspectionNotes"></h3>
                <h3> Description: <input type="text" v-model="Edits.Description"></h3>
                <h3> FileFolderURL: <input type="text" v-model="Edits.FileFolderURL"></h3>
                <h3> Type: <b-form-select size="sm" style="width: 75%;" v-model="Edits.InspectionType" :options="consts.CHOICE_FIELDS.AHJInspection.AHJInspectionType"/></h3>
                <h3> Technician Required: <input type="text" v-model="Edits.TechnicianRequired"></h3>
            </div>
        </div>
        <div style="border-right:none" class="info-div-insp">
            <!-- display all contacts. If editing, display add button -->
            <div style="text-align:center;padding:0px;width:100%;border-bottom:1px solid black;">Contacts<i v-if="this.isEditing" class="fa fa-plus add-cont" v-on:click="addACont()"/> </div>
        <contact-card v-for="contact in data.Contacts" v-bind:key="contact.ContactID.Value" v-bind:data="contact"/>
        </div>
        </div>
    </div>
</template>

<script>
import ContactCard from "./ContactCard.vue";
import constants from '../../constants.js';
import axios from "axios";

export default {
    props: {
        data: {
            type: Object
        },
        AHJPK: {
            type: Number
        },
        index: {
            type: Number
        },
        eID: {
            type: Number,
            default: -1
        },
        editStatus: {
            type: String,
            default: 'A'
        }
    },
    data(){
        return {
            //object to add a contact
            AddCont: {
                AHJPK: this.AHJPK,
                ParentTable: "AHJInspection",
                ParentID: null,
                SourceTable: "Contact",
                Value: []
            },
            isEditing: false,
            //deleted flag
            isDeleted: false,
            Type: "AHJInspection",
            Edits: {
                AHJInspectionName: "",
                AHJInspectionNotes: "",
                Description: "",
                FileFolderURL: "",
                InspectionType: "",
                TechnicianRequired: "" 
            },
            consts: constants,
            AddingConts: false,
            ID: "",
            //contact deletion object
            Deleted: {
                AHJPK: this.AHJPK,
                InspectionID: null,
                SourceTable: "Contact",
                Value: []
            },
            allContacts: [],
            editstatus: this.editStatus
        }
    },
    mounted(){
        this.$nextTick(() => {
        this.AddCont.ParentID = this.data.InspectionID.Value;
        this.ID = this.data.InspectionID.Value;
        this.AddCont.AHJPK = this.AHJPK;
        let k = Object.keys(this.Edits);
        for(let i = 0; i < k.length; i++){
            if(this.data[k[i]]){
                this.Edits[k[i]] = this.data[k[i]].Value;
            }
        }
        //agglomerate confirmed and unconfirmed contacts
        this.allContacts = [...this.data.UnconfirmedContacts,...this.data.Contacts];
        //set inspection ID in deleted object
        this.Deleted.InspectionID = this.data.InspectionID.Value;
        this.changeStatus();
        });
    },
    components: {
        "contact-card": ContactCard,
    },
    methods: {
        getPendingContacts(){
            //return contacts to be added
            return [...this.AddCont.Value];
        },
        changeStatus(){
            // is this is an edit object, change status on rejection / acceptance
            if(this.eID >= 0){
                if(this.editStatus === 'A'){
                    this.$refs.insp.style.backgroundColor = "#B7FFB3";
                }
                if(this.editStatus === 'R'){
                    this.$refs.insp.style.backgroundColor = "#FFBEBE";
                }
            
            }
        },
        addToContacts(conts){
            //add a contact to the contact addition object
            this.AddingConts = false;
            this.AddCont.Value = [...this.AddCont.Value, ...conts];
            return;
        },
        addACont(){
            //add a contact and open parent object contact addition window
            this.AddingConts = true;
            this.$parent.inspEditing = this.index;
            this.$parent.showBigDiv('addacontact');
        },
        getEditObjects(){
            //get edit objects on this Inpspection
            let editObjects = [];
            for(let i = 0; i < this.$children.length; i++){
                if(this.$children[i].Edits){
                    let e = this.$children[i].Edits;
                    let keys = Object.keys(e);
                    for(let j = 0; j < keys.length; j++){
                        if(this.$children[i].data[keys[j]] && this.$children[i].data[keys[j]].Value !== this.$children[i].Edits[keys[j]]){
                            //if value has been changed and is not "" return edit object
                            let obj = {};
                            obj['AHJPK'] = this.AHJPK;
                            obj['InspectionID'] = this.data.InspectionID.Value;
                            obj['SourceTable'] = this.$children[i].Type;
                            obj['SourceRow'] = this.$children[i].ID;
                            obj['SourceColumn'] = keys[j];
                            obj['OldValue'] = this.$children[i].data[keys[j]].Value;
                            obj['NewValue'] = this.$children[i].Edits[keys[j]];
                            editObjects.push(obj);
                        }
                    }
                    editObjects = editObjects.concat(this.$children[i].getEditObjects());
                }
            }
            return editObjects;
        },
        getDeletions(){
            //return all contact deletion objects
            this.Deleted.Value = [];
            for(let i = 0 ; i < this.$children.length; i++){
                if(this.$children[i].Type === "Contact" && this.$children[i].isDeleted){
                    this.Deleted.Value.push(this.$children[i].data.ContactID.Value);
                }
            }
        },
        delete(){
            //delete a contact using the API
            let url = constants.API_ENDPOINT + 'edit/delete/';
            axios
                .post(url,this.Deleted, {
                    headers: {
                        Authorization: this.$store.getters.authToken
                    }
                })
        },
        clearEdits(){
            //return all edit object value to their defaults
            let k = Object.keys(this.Edits);
            for(let i = 0; i < k.length; i++){
                if(k[i]==="Contacts" || this.data[k[i]] === null){
                    continue;
                }
                this.Edits[k[i]] = this.data[k[i]].Value;
            }
            this.isDeleted = false;
            //clear all edits on child contacts
            for(let i = 0; i < this.$children.length; i++){
                if(this.$children[i].Edits){
                    this.$children[i].clearEdits();
                }
            }
            this.AddCont.Value = [];
        },
        showInfo(){
            //toggle info div to show / hide
            this.$refs.hidden.classList.toggle('show');
            this.$refs.hidden.classList.toggle('hide');
            this.$refs.chev.classList.toggle('fa-chevron-down');
            this.$refs.chev.classList.toggle('fa-chevron-up');
        },
        undoStatusChange(){
            let url = constants.API_ENDPOINT + 'edit/undo/'
            axios
                .post(url,{ EditID: this.data.EditID }, {
                    headers: {
                        Authorization: this.$store.getters.authToken
                    }
                })
                .then(() => {
                    this.editstatus = 'P';
                    this.$refs.insp.style.backgroundColor = "white";
                })
                .catch(() => {
                    alert("Edit could not be undone, you may have edits that were applied after this one")
                })
        }
    },
    watch:{
        //if parent is editing, this object is editing
        '$parent.isEditing': function(){
            this.isEditing = this.$parent.isEditing;
        }
    }
}
</script>

<style scoped>
.inspection-card{
    position: relative;
    width: 100%;
    margin: 0;
    background-color: white;
}
.info-div-insp{
    display: flex;
    flex-direction: column;
    align-items: center;
    flex-basis: 50%;
        border-bottom: 1px solid black;
}
h3, a{
  font-size: 15px;
  margin: 0;
}
h2{
    margin: 0;
    width: calc(100% - 200px);
    margin-left: 100px;
    float: left;
}
.plus-button{
    position: absolute;
    top: 10px;
    right: 5px;
}
.add-cont{
    float: right;
    margin-right: 5px;
    margin-top: 2px;
}
.header{
    width: 100%;
    border-bottom: 1px solid black;
    text-align: center;
    height: 40px;
    display: flex;
    justify-content: space-between;
}
.body{
    width: 100%;
    display: flex;
    flex-wrap: wrap;
}
.hide{
    display: none;
}
.show{
    display: flex;
}
.head{
    margin: 0;
    width: calc(100% - 200px);
    margin-left: 100px;
    float: left;
}
</style>