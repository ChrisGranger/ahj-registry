<template>
    <div ref="err" class="erreq">
        <div class="header">
            <!-- display ERR type as head of this object -->
            <h2>{{ (this.data.EngineeringReviewType === null || this.data.EngineeringReviewType.Value === "") && !this.isEditing ? "Unspecified" : this.isEditing ? "" : this.data.EngineeringReviewType.Value}} <b-form-select size="sm" style="width:75%" v-if="isEditing" v-model="Edits.EngineeringReviewType" :options="consts.CHOICE_FIELDS.EngineeringReviewRequirement.EngineeringReviewType"/> </h2>
            <div style="display:flex">
            <div style="width: 50px;margin-right:10px;" v-if="eID >= 0">
                <i style="margin-right:10px;margin-top:10px;" v-if="$parent.isManaged && this.editstatus==='P'" v-on:click="$emit('official',{Type:'Accept',eID: eID});editstatus = 'A';changeStatus();" class="fa fa-check"></i>
                <i style="margin-right:5px;" v-if="$parent.isManaged && this.editstatus==='P'" v-on:click="$emit('official',{Type:'Reject',eID: eID});editstatus='R';changeStatus();" class="fa fa-times"></i>
                <i v-if="$parent.isManaged && this.data.ReviewStatus!=='P'" v-on:click="undoStatusChange()" class="fas fa-undo"></i>
            </div>
            <i ref='chev' style="height:100%;margin-right: 10px;margin-top:10px;" class="fa fa-chevron-down" v-on:click="showInfo()"></i>
            <div style="float: right;" v-if="isEditing">
                <!-- button to delete this ERR -->
                <i v-if="!isDeleted" ref='del' style="margin-right: 10px;margin-top:10px;" v-on:click="isDeleted = true" class="fa fa-minus"></i>
                <i v-else v-on:click="isDeleted=false" style="margin-right: 10px;margin-top:10px;" class="fas fa-exclamation-triangle"></i>
            </div>
            </div>
        </div>
        <div style="width:100%;" ref="hidden" class="hide">
            <!-- info to display -->
        <div style="width:100%;" v-if="!isEditing">
                <div class="flex-vert">
                    <h3> Requirement Level: {{ (this.data.RequirementLevel === null || this.data.RequirementLevel.Value === "")  ? "Unspecified" : this.data.RequirementLevel.Value}} </h3>
                    <h3> Requirement Notes: {{ (this.data.RequirementNotes === null || this.data.RequirementNotes.Value === "") ? "Unspecified" : this.data.RequirementNotes.Value}} </h3>
                    <h3 > Stamp Type: {{ (this.data.StampType === null || this.data.StampType.Value === "")  ? "Unspecified" :  this.data.StampType.Value}} </h3>
                    <h3> Description: {{ (this.data.Description === null || this.data.Description.Value === "") ? "Unspecified" : this.data.Description.Value}} </h3>
                </div>
        </div>
        <!-- if is editing, display text boxes -->
        <div style="width:100%;" v-else>
            <div class="flex-vert">
            <h3> Requirement Level: <b-form-select size="sm" style="width:50%" v-if="isEditing" v-model="Edits.RequirementLevel" :options="consts.CHOICE_FIELDS.EngineeringReviewRequirement.RequirementLevel"/></h3>
            <h3> Requirment Notes: <input v-if="isEditing" type="text" v-model="Edits.RequirementNotes" /> </h3>
            <h3 style="width:50%;"> Stamp Type: <b-form-select style="width:50%;" size="sm" v-if="isEditing" v-model="Edits.StampType" :options="consts.CHOICE_FIELDS.EngineeringReviewRequirement.StampType"/></h3>
            <h3> Description: <input style="flex-basis:100%;" v-if="isEditing" type="text" v-model="Edits.Description" /> </h3>
            </div>
        </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import constants from '../../constants.js';

export default {
    props: {
        data: {
            type: Object
        },
        editing:{
            type: Boolean
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
            isEditing: this.editing,
            //object type as string
            Type: "EngineeringReviewRequirements",
            editable: true,
            consts: constants,
            //edit object
            Edits: {
                EngineeringReviewType: "",
                RequirementLevel: "",
                RequirementNotes: "",
                StampType: "",
                Description: ""
            },
            //deleted flag
            isDeleted: false,
            ID: -1,
            editstatus: this.editStatus
        }
    },
    created: function(){
        //on created set values in edits table and ID
        let k = Object.keys(this.Edits);
        for(let i = 0; i < k.length; i++){
            this.Edits[k[i]] = this.data[k[i]].Value;
        }
        this.ID = this.data.EngineeringReviewRequirementID.Value;
    },
    mounted: function(){
        this.changeStatus();
    },
    methods: {
        clearEdits(){
            //clear all edits on this ERR
            let keys = Object.keys(this.Edits);
            for(let i = 0; i < keys.length; i++){
                this.Edits[keys[i]] = this.data[keys[i]].Value;
            }
            this.isDeleted = false;
        },
        getEditObjects(){
            //no child object can be edited
            return [];
        },
        changeStatus(){
            //change status to accepted / rejected
            if(this.eID >= 0){
                if(this.editStatus === 'A'){
                    if(this.$refs.err){
                        this.$refs.err.style.backgroundColor = "#B7FFB3";
                    }
                }
                if(this.editStatus === 'R'){
                    if(this.$refs.err){
                        this.$refs.err.style.backgroundColor = "#FFBEBE";
                    }
                }
            
            }
        },
        showInfo(){
            //toggle the info dropdown to show / hide
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
                    this.$refs.err.style.backgroundColor = "white";
                })
                .catch(() => {
                    alert("Edit could not be undone, you may have edits that were applied after this one")
                })
        }
    },
    watch: {
        '$parent.isEditing': function() {
            //if parent object is editing, this object is editing
            this.isEditing = this.$parent.isEditing;
        }
    }
}
</script>

<style scoped>
.erreq{
    width: 100%;
    background-color: white;
}
.flex-hor{
    display: flex;
    flex-wrap: wrap;
    flex-direction: row;
}
.flex-vert{
    display: flex;
    flex-direction: column;
    margin: 0px;
    border-bottom: 1px solid black;
    width: 100%;
    align-items: center;
}
h3, a{
  font-size: 15px;
  margin: 0px;
}
.header{
    width: 100%;
    border-bottom: 1px solid black;
    text-align: center;
    height: 40px;
    display: flex;
    justify-content: space-between;
}
h2{
    margin: 0;
    width: calc(100% - 200px);
    margin-left: 100px;
    float: left;
}
.hide{
    display: none;
}
.show{
    display: flex;
}
</style>