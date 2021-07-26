<template>
    <div ref="cc" id="contactCard">
        <div id="header">
            <!-- use name as header, if editing, display as text box -->
            <h2 v-if="!isEditing" style="margin-left: 5px;">{{this.data.FirstName.Value + " " + this.data.LastName.Value}}</h2>
            <div v-else style="display:flex;width:100%;flex-wrap:wrap;">
                <input style="flex-basis:33%;" type="text" v-model="Edits.FirstName">
                <input style="flex-basis:33%;" type="text" v-model="Edits.MiddleName">
                <input style="flex-basis:33%;" type="text" v-model="Edits.LastName">
            </div>
            <div style="display:flex;margin-right:10px;">
                            <div v-if="eID >= 0">
                                <!-- if this is an edit object and user manages this AHJ, allow acceptance / rejections -->
            <i style="margin-right:10px" v-if="$parent.isManaged && editstatus==='P'" v-on:click="$emit('official',{Type:'Accept',eID: eID});editstatus = 'A';changeStatus();" class="fa fa-check"></i>
            <i style="margin-right:10px" v-if="$parent.isManaged && editstatus==='P'" v-on:click="$emit('official',{Type:'Reject',eID: eID});editstatus='R';changeStatus()" class="fa fa-times"></i>
            <i v-if="$parent.isManaged && editstatus !=='P'" v-on:click="undoStatusChange()" class="fas fa-undo"></i>
            </div>
            <div style="display:flex;" v-if="isEditing">
                <i ref='chev' style="height:100%;margin-right: 10px;" class="fa fa-chevron-down" v-on:click="showInfo('c-info')"></i>
                <!-- button to delete this COntact -->
                <i v-if="!isDeleted" ref='del' style="height:100%;margin-right: 10px;" v-on:click="isDeleted = true" class="fa fa-minus"></i>
                <i v-else v-on:click="isDeleted=false" style="height:100%;margin-right: 10px;" class="fas fa-exclamation-triangle"></i>
            </div>
            <div v-else>
                <i ref='chev' style="height:100%;margin-right: 10px;" class="fa fa-chevron-down" v-on:click="showInfo('c-info')"></i>
            </div>
            </div>
        </div>
        <div ref="c_info" class="hide">
            <!-- div to show title, text box if editing -->
            <div class='title-div'>
                <h3 style="margin:0px;" v-if="!isEditing"> {{this.data.Title === null ? "No Title" : this.data.Title.Value}} </h3>
                <input v-else type="text" v-model="Edits.Title"/>
            </div>
            <!-- contact info or text boxes if editing -->
            <div class='info-div'>
                <div class='phone-info'>
                    <h3> Home Phone: {{(this.data.HomePhone === null || this.data.HomePhone.Value === "") && !this.isEditing ? "Unspecified" : this.isEditing ? "" : this.data.HomePhone.Value}}<input v-if="isEditing" v-model="Edits.HomePhone"/>  </h3>
                    <h3> Mobile Phone: {{(this.data.MobilePhone === null || this.data.MobilePhone.Value === "") && !this.isEditing ? "Unspecified" : this.isEditing ? "" : this.data.MobilePhone.Value}}<input v-if="isEditing" v-model="Edits.MobilePhone"/> </h3>
                    <h3> Work Phone: {{(this.data.WorkPhone === null || this.data.WorkPhone.Value === "") && !this.isEditing ? "Unspecified" : this.isEditing ? "" : this.data.WorkPhone.Value}}<input v-if="isEditing" v-model="Edits.WorkPhone"/></h3>
                    <h3> URL: {{(this.data.URL === null || this.data.URL.Value === "") && !this.isEditing ? "Unspecified" : this.isEditing ? "" : this.data.URL.Value}}<input v-if="isEditing" v-model="Edits.URL"/></h3>
                    <h3> Email: {{(this.data.Email === null || this.data.Email.Value === "") && !this.isEditing ? "Unspecified" : this.isEditing ? "" : this.data.Email.Value}}<input v-if="isEditing" v-model="Edits.Email"/> </h3>
                    <h3> Preferred Contact Method: {{(this.data.PreferredContactMethod === null || this.data.PreferredContactMethod.Value === "") && !this.isEditing ? "Unspecified" : this.isEditing ? "" : this.data.PreferredContactMethod.Value}}<input v-if="isEditing" v-model="Edits.PreferredContactMethod"/> </h3>
                </div>
                <!-- Address (not editable) -->
                <div id="addr" class='addr-info'>
                    <div v-if="!isEditing">
                        <h3 class="desc" v-if="this.AddressString !== ''">{{this.AddressString}}</h3>
                        <h3 class="desc" v-else>No Address Provided</h3>
                    </div>
                    <div class="desc" v-else>
                        <a style="text-decoration: underline; cursor:pointer;font-size:15px;" v-on:click="editAddress()">Edit this address</a>
                    </div>
                </div>
                <!-- Description or text box of editable -->
                <div class="desc">
                    <h3>{{(this.data.Description === null || this.data.Description.Value === "") && !this.isEditing ? "Unspecified" : this.isEditing ? "" : this.data.Description.Value}}<input v-if="isEditing" v-model="Edits.Description"/></h3>
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
        editing: {
            type: Boolean
        },
        eID: {
            type: Number,
            default: -1
        },
        editStatus: {
            type: String,
            default: 'A'
        },
    },
    data() {
        return {
            isEditing: this.editing,
            //address format strings
            AddressString: "",
            CityCountyState: "",
            isDeleted: false,
            Type: "Contact",
            editable: true,
            ID: -1,
            //edit object
            Edits: {
                Title: this.data.Title ? this.data.Title.Value : "",
                HomePhone: this.data.HomePhone ? this.data.HomePhone.Value : "",
                MobilePhone: "",
                WorkPhone: "",
                URL: "",
                Email: "",
                PreferredContactMethod: "",
                Description: "",
                FirstName: "",
                MiddleName: "",
                LastName: ""
            },
            editstatus: this.editStatus
        }
    },
    mounted: function() {
        //fires after mount
        this.$nextTick(()=>{
            //format the address
        if(this.data.Address){
            this.formatAddress(this.data.Address);
        }
        // this.ID = this.data.ContactID.Value;
        //clear all edits
        this.clearEdits();
        });
        this.changeStatus();
        this.ID = this.data.ContactID.Value;
    },
    methods:{
        showInfo(){
            //toggle show / hide info div
            this.$refs.c_info.classList.toggle('show');
            this.$refs.c_info.classList.toggle('hide');
            this.$refs.chev.classList.toggle('fa-chevron-down');
            this.$refs.chev.classList.toggle('fa-chevron-up');
        },
        changeStatus(){
            //if this is an edit object, change to allow rejection / acceptance
            if(this.eID >= 0){
                if(this.editStatus === 'A'){
                    this.$refs.cc.style.backgroundColor = "#B7FFB3";
                }
                if(this.editStatus === 'R'){
                    this.$refs.cc.style.backgroundColor = "#FFBEBE";
                }
            
            }
        },
        formatAddress(Address){
                this.AddressString = "";
            this.CityCountyState = "";
            //if no first values, address string is empty
            if(Address.AddrLine1.Value === "" && Address.AddrLine2.Value === "" && Address.AddrLine3.Value === ""){
                this.AddressString = "";
            }
            else{
                //add line 1
                if(Address.AddrLine1.Value !== ""){
                    this.AddressString += Address.AddrLine1.Value;
                }
                //add line 2, and comma if needed
                if(Address.AddrLine2.Value !== ""){
                    if(this.AddressString !== ""){
                        this.AddressString += ', ';
                    }
                    this.AddressString += Address.AddrLine2.Value;
                }//add line 3 and comma if needed
                if(Address.AddrLine3.Value !== ""){
                    if(this.AddressString !== ""){
                        this.AddressString += ', '
                    }
                    this.AddressString += Address.AddrLine3.Value;
                }
                this.CityCountyState = "";
            }
            // add comma before city county state fields, if necessary
            //add city
            if(Address.City.Value !== ""){
                if(this.AddressString !== ""){
                    this.CityCountyState += ', ';
                }
                this.CityCountyState += Address.City.Value;
            }
            //add county and comma if necessary
            if(Address.County.Value !== ""){
                if(this.CityCountyState !== "" || this.AddressString !== ''){
                    this.CityCountyState += ", ";
                }
                this.CityCountyState += Address.County.Value;
            }
            //add state and comma if necessary
            if(Address.StateProvince.Value !== ""){
                if(this.CityCountyState !== "" || this.AddressString !== ''){
                    this.CityCountyState += ", "
                }
                this.CityCountyState += Address.StateProvince.Value;
            }
            //add country andf comma if necessary
            if(Address.Country.Value !== ""){
                if(this.CityCountyState !== "" || this.AddressString !== ''){
                    this.CityCountyState += ", "
                }
                this.CityCountyState += Address.Country.Value;
            }
            //add zip code and comma if necessary
            if(Address.ZipPostalCode.Value !== ""){
                if(this.CityCountyState !== "" || this.AddressString !== ''){
                    this.CityCountyState += ", "
                }
                this.CityCountyState += Address.ZipPostalCode.Value;
            }
            //add city/county/state to toal address
            this.AddressString = this.AddressString + this.CityCountyState;
        },
        clearEdits(){
            //return all edit object fields to default
            let keys = Object.keys(this.Edits);
            for(let i = 0; i < keys.length; i++){
                this.Edits[keys[i]] = this.data[keys[i]].Value;
            }
            this.isDeleted = false;
        },
        getEditObjects(){
            // no editable child objects
            return [];
        },
        editAddress(){
            this.$parent.changeCont(this.data.ContactID.Value);
            this.$parent.editingCont = this.data.ContactID.Value;
            this.$parent.editingCont = this.ID;
            this.$parent.setAddrAndLocation();
            this.$parent.showBigDiv('addressLoc');
        },
        undoStatusChange(){
            let url = constants.API_ENDPOINT + 'edit/undo/'
            axios
                .post(url,{ EditID: this.eID }, {
                    headers: {
                        Authorization: this.$store.getters.authToken
                    }
                })
                .then(() => {
                    this.editstatus = 'P';
                    this.$refs.cc.style.backgroundColor = "white";
                })
                .catch(() => {
                    alert("Edit could not be undone, you may have edits that were applied after this one")
                })
        }
    },
    watch: {
        //if parent is editing so are we
        '$parent.isEditing': function() {
            this.isEditing = this.$parent.isEditing;
        }
    }
}
</script>

<style scoped>
h1,h2,h3{
    font-family: "Roboto Condensed";
    color: #4b4e52;
}
h3{
    font-size: 10px;
    margin: 0px;
}
.info-header{
    font-size: 10px;
    margin: 0px;
}
#contactCard{
    position: relative;
    width: 100%;
    margin: 0;
    display: flex;
    flex-direction: column;
    border-bottom: 1px solid black;
    background-color: white;
}
#header{
    display: flex;
    align-items: center;
    justify-content: space-between;
}
#c-info{
    position: relative;
    width: 100%;
    border-top: 1px solid black;
    background-color: white;
}
.show{
    display: table;
}
.hide{
    display: none;
}
.title-div{
    position: relative;
    border-bottom: 1px solid gray;
    border-top: 1px solid black;
}
.phone-info{
    position: relative;
    width: 100%;
    display: flex;
    justify-content: center;
    flex-direction: column;
    align-items: center;
}
.addr-info{
    position: relative;
    width: 100%;
}
.info-div{
    position: relative;
    width: 100%;
    overflow: auto;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
}
.no-data{
    padding-top: 11%;
}
.desc{
    text-align: center;
    width: 100%;
    border-top: 1px solid gray;
}
.bb{
    border-bottom: 1px solid black;
}
</style>