<template>
    <div ref="eobj" id="edit-object">
        <!-- show info about this edit -->
        <h3>{{this.data.DateRequested}}</h3>
        <h3>Changed "{{this.data.OldValue == null || this.data.OldValue == "" ? "None" : this.data.OldValue}}" to "{{this.data.NewValue}}"</h3>
        <h3>Comments: "{{this.data.Comments == "" || this.data.Comments == null ? "No Comments" : this.data.Comments}}"</h3>
        <h3>{{this.data.ChangedBy ? this.data.ChangedBy : "Anonymous"}}</h3>
        <div style="margin-right:10px;">
            <i style="margin-right:10px" v-if="$parent.isManaged && this.data.ReviewStatus==='P'" v-on:click="$emit('official',{Type:'Accept',eID: data.EditID});data.ReviewStatus='A';changeStatus();" class="fa fa-check"></i>
            <i v-if="$parent.isManaged && this.data.ReviewStatus==='P'" v-on:click="$emit('official', {Type:'Reject',eID: data.EditID});data.ReviewStatus='R';changeStatus()" class="fa fa-times"></i>
        </div>
    </div>
</template>

<script>
import moment from "moment";

export default {
    props: {
        data: {
            type: Object
        }
    },
    data(){
        return {
            EditDate: ""
        }
    },
    mounted: function(){
        this.changeStatus();
        this.data.DateRequested = moment(this.data.DateRequested).format('MMMM Do YYYY, h:mm:ss a');
    },
    methods: {
        //change edit status on acceptance / rejection
        changeStatus(){
                if(this.data.ReviewStatus === 'A'){
                    this.$refs.eobj.style.backgroundColor = "#B7FFB3";
                }
                if(this.data.ReviewStatus === 'R'){
                    this.$refs.eobj.style.backgroundColor = "#FFBEBE";
                }
        },
    }
}
</script>

<style scoped>
#edit-object{
    display: flex;
    justify-content: space-between;
    align-content: center;
    align-items: center;
    padding: 10px;
    background-clip: content-box;
    background-color: white;
}
h1,h2,h3{
    font-family: "Roboto Condensed";
    color: #4b4e52;
    width: 20%;
}
h3{
    font-size: 15px;
    margin: 0px;
}
#content-body{
    display: flex;
    flex-direction: column;
}
</style>