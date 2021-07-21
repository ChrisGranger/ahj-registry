<template>
    <div ref='page'>
        <!-- Window to confirm edits, this window is hidden until user clicks "Submit Edits" button -->
        <div id="confirm-edits" class='edits hide'>
            <div style="width:15px;height:15px;top:0px;float:right;position:sticky;color:red;" v-on:click="showBigDiv('confirm-edits')" class="fas fa-times"></div>
            <div class="big-div">
                <div class="edit-title">Edits</div>
                <!-- Diplay all changes made on any field -->
                <div style="display: flex; align-items:center; flex-direction:column;">
                    <div style="display:flex; justify-content:space-between;background-color: white; width:81%;" v-for="(edit,index) in editObjects" v-bind:key="`EDIT${index}`">
                        <h3>You have changed {{edit.OldValue}} to {{edit.NewValue}} for {{edit.SourceColumn}}</h3>
                        <!-- Allow an edit to be deleted before submitting -->
                        <i v-on:click="deleteEdit(index)" class="fas fa-minus"></i>
                    </div>
                </div>
                <div class="edit-title">Additions</div>
                <!-- Display all additions made -->
                <div style="display: flex; align-items:center; flex-direction:column;">
                    <div style="display:flex; justify-content:space-between;background-color: white; width:81%;" v-for="(add,index) in contactAddition.Value" v-bind:key="`CONTADD${index}`">
                        <h3>You have added a Contact</h3>
                        <!-- Allow it to be deleted -->
                        <i v-on:click="deleteContactAddition(index)" class="fas fa-minus"></i>
                    </div>
                    <div style="display:flex; justify-content:space-between;background-color: white; width:81%;" v-for="(add,index) in $children" v-bind:key="`INSPChil${index}`">
                        <div v-if="add.Type==='AHJInspection'">
                            <div v-for="(a,i) in add.AddCont.Value" v-bind:key="`INSPCONT${i}`">
                                <!-- Contact added to an inspection -->
                                <h3>You have added a Contact to an AHJInspection: {{ add.data.AHJInspectionName.Value }}</h3>
                                <!-- Delete the added contact -->
                                <i v-on:click="deleteInspectionContactAddition(index,i)" class="fas fa-minus"></i>
                            </div>
                        </div>
                    </div>
                    <div style="display:flex; justify-content:space-between;background-color: white; width:81%;" v-for="(add,index) in inspectionAddition.Value" v-bind:key="`INSP${index}`">
                        <h3>You have added an Inspection</h3>
                        <!-- Delete the added inspection -->
                        <i v-on:click="deleteInspectionAddition(index)" class="fas fa-minus"></i>
                    </div>
                    <div style="display:flex; justify-content:space-between;background-color: white; width:81%;" v-for="(add,index) in AddPIM.Value" v-bind:key="`PIM${index}`">
                        <h3>You have added a Permit Issue Method</h3>
                        <!-- Delete added Permit Issue Method -->
                        <i v-on:click="deletePIMAddition(index)" class="fas fa-minus"></i>
                    </div>
                    <div style="display:flex; justify-content:space-between;background-color: white; width:81%;" v-for="(add,index) in AddDSM.Value" v-bind:key="`DSM-${index}`">
                        <h3>You have added a Document Submission Method</h3>
                        <!-- Delete Added DSM -->
                        <i v-on:click="deleteDSMAddition(index)" class="fas fa-minus"></i>
                    </div>
                    <div style="display:flex; justify-content:space-between;background-color: white; width:81%;" v-for="(add,index) in ERRAddition.Value" v-bind:key="`ERR-${index}`">
                        <h3>You have added an Engineering Review Requirement</h3>
                        <!-- Delete Added ERR -->
                        <i v-on:click="deleteERRAddition(index)" class="fas fa-minus"></i>
                    </div>
                    <div style="display:flex; justify-content:space-between;background-color: white; width:81%;" v-for="(add,index) in FSAddition.Value" v-bind:key="`FS-${index}`">
                        <h3>You have added a Fee Structure</h3>
                        <!-- Delete Added Fee Structures -->
                        <i v-on:click="deleteFSAddition(index)" class="fas fa-minus"></i>
                    </div>
                </div>
                <div class="edit-title">Deletions</div>
                <div style="display: flex; align-items:center; flex-direction:column;">
                    <div style="display:flex; justify-content:space-between;background-color: white; width:81%;" v-for="(del,index) in contactDeletions.Value" v-bind:key="`CONTD-${index}`">
                        <h3>You have deleted a Contact</h3>
                        <!-- Remove Contact Deletion -->
                        <i v-on:click="deleteContactDeletion(index)" class="fas fa-minus"></i>
                    </div>
                    <div style="display:flex; justify-content:space-between;background-color: white; width:81%;" v-for="(del,index) in inspectionDeletions.Value" v-bind:key="`INSPD-${index}`">
                        <h3>You have deleted an Inspection</h3>
                        <!-- Remove Inspection Deletion -->
                        <i v-on:click="deleteInspectionDeletion(index)" class="fas fa-minus"></i>
                    </div>
                    <div style="display:flex; justify-content:space-between;background-color: white; width:81%;" v-for="(add,index) in $children" v-bind:key="`INSPCD-${index}`">
                        <div v-if="add.Type==='AHJInspection'">
                            <div v-for="(a,i) in add.Deleted.Value" v-bind:key="`INPSCDC-${i}`">
                                <!-- Delete Inspection Contact -->
                                <h3>You have deleted a Contact on AHJInspection: {{ add.data.AHJInspectionName.Value }}</h3>
                                <!-- Remove Inspection Contact Deletion --> 
                                <i v-on:click="deleteContonInsp(index,i)" class="fas fa-minus"></i>
                            </div>
                        </div>
                    </div>
                    <div style="display:flex; justify-content:space-between;background-color: white; width:81%;" v-for="(del,index) in ERRDeletions.Value" v-bind:key="`ERRD-${index}`">
                        <h3>You have deleted an Engineering Review Requirement</h3>
                        <!-- Remove ERR deletion -->
                        <i v-on:click="deleteERRDeletion(index)" class="fas fa-minus"></i>
                    </div>
                    <div style="display:flex; justify-content:space-between;background-color: white; width:81%;" v-for="(del,index) in FSDeletions.Value" v-bind:key="`FSD-${index}`">
                        <h3>You have deleted a Fee Structure</h3>
                        <!-- Remove Fee Structure Deletion -->
                        <i v-on:click="deleteFSDeletion(index)" class="fas fa-minus"></i>
                    </div>
                    <div style="display:flex; justify-content:space-between;background-color: white; width:81%;" v-for="(del,index) in DSMDeletion.Value" v-bind:key="`DSMD-${index}`">
                        <h3>You have deleted a Document Submission Method</h3>
                        <!-- Remove DSM Deletion -->
                        <i v-on:click="DSMDeletion.Value.splice(index,1)" class="fas fa-minus"></i>
                    </div>
                    <div style="display:flex; justify-content:space-between;background-color: white; width:81%;" v-for="(del,index) in PIMDeletion.Value" v-bind:key="`PIMD-${index}`">
                        <h3>You have deleted a Permit Issue Method</h3>
                        <!-- Remove PIM Deletion -->
                        <i v-on:click="PIMDeletion.Value.splice(index,1)" class="fas fa-minus"></i>
                    </div>
                </div>
                <div class="edit-buttons">
                    <!-- This button will submit all edits to the backend -->
                    <a style="margin:0;padding:0;text-decoration: underline;margin-right:10px;" v-on:click="submitEdits()">Submit Edits</a>
                    <!-- This button will close the Window WITHOUT DELETING EDITS -->
                    <a style="margin:0;padding:0;text-decoration: underline;" v-on:click="showBigDiv('confirm-edits')">Cancel</a>
                </div>
            </div>
        </div>
        <!-- Window to add a contact -->
        <div id='addacontact' class='edits hide'>
            <div style="width:15px;height:15px;top:0px;float:right;position:sticky;color:red;" v-on:click="showBigDiv('addacontact')" class="fas fa-times"></div>
            <div class="big-div">
                <div style="margin:2px;">Add a Contact</div>
                <div style="margin:2px;margin-top:0px;margin-bottom:25px;border-bottom:1px solid black;height:0px;"></div>
                <div class="add-cont">
                    <!-- These are all the necessary fields to add a contact -->
                        <div class="add-breakup">
                        <label for="FirstName">First Name</label>
                        <input type="text" v-model="AddCont.FirstName" class="form-control" id="FirstName" placeholder="First Name">
                        <label for="MiddleName">Middle Name</label>
                        <input type="text" v-model="AddCont.MiddleName" class="form-control" id="MiddleName" placeholder="Middle Name">
                        <label for="LastName">Last Name</label>
                        <input type="text" v-model="AddCont.LastName" class="form-control" id="LastName" placeholder="Last Name">
                        </div>
                        <div class="add-breakup">
                        <label for="WorkPhone">Work Phone</label>
                        <input type="text" v-model="AddCont.WorkPhone" class="form-control" id="WorkPhone" placeholder="Work Phone">
                        <label for="HomePhone">Home Phone</label>
                        <input type="text" v-model="AddCont.HomePhone" class="form-control" id="HomePhone" placeholder="Home Phone">
                        <label for="MobilePhone">Mobile Phone</label>
                        <input type="text" v-model="AddCont.MobilePhone" class="form-control" id="MobilePhone" placeholder="Mobile Phone">
                        </div>
                        <div class="add-breakup">
                        <label for="Email">Email</label>
                        <input type="text" v-model="AddCont.Email" class="form-control" id="Email" placeholder="Email">
                        <label for="URL">URL</label>
                        <input type="text" v-model="AddCont.URL" class="form-control" id="URL" placeholder="URL">
                        <label for="Description">Description</label>
                        <input type="text" v-model="AddCont.Description" class="form-control" id="Description" placeholder="Description">
                        </div>
                        <div class="add-breakup">
                        <label for="Title">Title</label>
                        <input type="text" id="Title" v-model="AddCont.Title" class="form-control" placeholder="Title"/>
                        <label for="TimeZone">Time Zone</label>
                        <input type="text" v-model="AddCont.ContactTimezone" class="form-control" id="TimeZone" placeholder="Time Zone">
                        <label for="Type">Contact Type</label>
                        <b-form-select size="sm" id="Type" :options="consts.CHOICE_FIELDS.Contact.ContactType" v-model="AddCont.ContactType" />
                        <label for="pcm">Preferred Contact Method</label>
                        <b-form-select size="sm" id="Type" :options="consts.CHOICE_FIELDS.Contact.PreferredContactMethod" v-model="AddCont.PreferredContactMethod" />
                        </div>
                        <div style="flex-basis: 100%;margin-bottom:50px;"/>
                        <div class="add-breakup">
                        <label for="Line1">Address Line 1</label>
                        <input type="text" v-model="Address.AddrLine1" class="form-control" id="Line1" placeholder="Line 1">
                        <label for="Line2">Address Line 2</label>
                        <input type="text" v-model="Address.AddrLine2" class="form-control" id="Line2" placeholder="Line 2">
                        <label for="Line3">Address Line 3</label>
                        <input type="text" v-model="Address.AddrLine3" class="form-control" id="Line3" placeholder="Line 3">
                        </div>
                        <div class="add-breakup">
                        <label for="city">City</label>
                        <input type="text" v-model="Address.City" class="form-control" id="city" placeholder="City">
                        <label for="county">County</label>
                        <input type="text" v-model="Address.County" class="form-control" id="county" placeholder="County">
                        <label for="s/p">State/Province</label>
                        <input type="text" v-model="Address.StateProvince" class="form-control" id="s/p" placeholder="State/Province">
                        <label for="country">Country</label>
                        <input type="text" v-model="Address.Country" class="form-control" id="country" placeholder="Country">
                        </div>
                        <div class="add-breakup">
                        <label for="zip">ZIP Code</label>
                        <input type="text" v-model="Address.ZipPostalCode" class="form-control" id="zip" placeholder="ZIP Code">
                        <label for="addrtype">Address Type</label>
                         <b-form-select size="sm" id="addrtype" :options="consts.CHOICE_FIELDS.Address.AddressType" v-model="Address.AddressType" />
                        <label for="Description">Description</label>
                        <input type="text" v-model="Address.Description" class="form-control" id="Description" placeholder="Description">
                        </div>
                        <div class="add-breakup">
                        <label for="locdesc">Location Description</label>
                        <input type="text" v-model="Location.Description" class="form-control" id="locdesc" placeholder="Location Description" />
                        <label for="detmeth">Location Determination Method</label>
                         <b-form-select size="sm" id="detmeth" :options="consts.CHOICE_FIELDS.Location.LocationDeterminationMethod" v-model="Location.LocationDeterminationMethod" />
                         <label for="loctype">Location Type</label>
                         <b-form-select size="sm" id="loctype" :options="consts.CHOICE_FIELDS.Location.LocationType" v-model="Location.LocationType" />
                        </div>
                </div>
                
                <div style="margin:2px;margin-top:15px;">Created Contacts</div>
                <div style="margin:2px;margin-top:0px;margin-bottom:25px;border-bottom:1px solid black;height:0px;"></div>
                <div v-if="inspEditing < 0">
                <div style="display: flex; align-items:center; flex-direction:column;">
                <!-- This will display created contacts -->
                <div style="display:flex; justify-content:space-between;background-color: white; width:900px;" v-for="(c,index) in this.contactAddition.Value" v-bind:key="`addedc-${index}`" v-bind:data="c.Value">
                    <h3>You have added a Contact: {{c.FirstName}}</h3>
                    <!-- Delete a created contact -->
                    <i v-on:click="deleteCont(index)" class="fas fa-minus"></i>
                    <!-- Fill in text input boxes with this contacts information to allow user to change it -->
                    <i v-on:click="returnCont(index)" class="fas fa-pencil-alt"></i>
                </div>
                </div>
                </div>
                <div v-else>
                <div style="display: flex; align-items:center; flex-direction:column;">
                    <!-- This displays contacts added to an inspection -->
                <div style="display:flex; justify-content:space-between;background-color: white; width:900px;" v-for="(c,index) in this.AdditionOnInsp" v-bind:key="`addedctoi-${index}`" v-bind:data="c.Value">
                    <h3>You have added a Contact: {{c.FirstName}} to an Inspection</h3>
                     <!-- Delete a created contact -->
                    <i v-on:click="deleteCont(index)" class="fas fa-minus"></i>
                    <!-- Fill in text input boxes with this contacts information to allow user to change it -->
                    <i v-on:click="returnCont(index)" class="fas fa-pencil-alt"></i>
                </div>
                </div>
                </div>
                <div class="edit-buttons">
                    <!-- Adds contact to list of current contacts -->
                    <a style="margin:0;padding:0;text-decoration: underline;margin-right:10px;" v-on:click="addContact()">{{(this.replacingCont == -1) ?  "Add" : "Save"}}</a>
                    <!-- Closes the window without adding contact to list -->
                    <a style="margin:0;padding:0;text-decoration: underline;" v-on:click="showBigDiv('addacontact')">Cancel</a>
                </div>
            </div>
        </div>
        <!-- Window to add an AHJInspection -->
        <div id='addainspection' class='edits hide'>
            <div style="width:15px;height:15px;top:0px;float:right;position:sticky;color:red;" v-on:click="showBigDiv('addainspection')" class="fas fa-times"></div>
            <div class="big-div">
                <div style="margin:2px;">Add an Inspection</div>
                <div style="margin:2px;margin-top:0px;margin-bottom:25px;border-bottom:1px solid black;height:0px;"/>
                <div class="add-cont">
                    <!-- Fields necessary to add an inspeciton as text input boxes -->
                    <div class="add-breakup" style="flex-basis:45%;">
                        <label for="iname">Inspection Name</label>
                        <input type="text" v-model="AddInsp.AHJInspectionName" class="form-control" id="iname" placeholder="Inspection Name">
                        <label for="inotes">Inspection Notes</label>
                        <textarea v-model="AddInsp.AHJInspectionNotes" class="form-control" id="inotes" placeholder="Inspection Notes"/>
                        <label for="desc">Description</label>
                        <input type="text" v-model="AddInsp.Description" class="form-control" id="desc" placeholder="Description">
                    </div>
                    <div class="add-breakup" style="flex-basis:45%;">
                        <label for="url">File Folder URL</label>
                        <input type="text" v-model="AddInsp.FileFolderURL" class="form-control" id="url" placeholder="URL">
                        <label for="type">Inspection Type</label>
                        <b-form-select size="sm" id="type" v-model="AddInsp.InspectionType" :options="consts.CHOICE_FIELDS.AHJInspection.AHJInspectionType" style="width:155px;"></b-form-select>
                        <label for="tech">Technician Required?</label>
                        <b-form-select size="sm" id="type" v-model="AddInsp.TechnicianRequired" :options="technicianRequiredOptions" style="width:155px;"></b-form-select>
                    </div>
                    <!-- Allows user to add a contact with their inspection addition -->
                    <div style="margin:2px;margin-top:25px;flex-basis:100%;">Add Contacts</div>
                    <div style="margin:2px;margin-top:0px;margin-bottom:25px;border-bottom:1px solid black;height:0px;flex-basis:100%;"/>
                    <div class="add-cont" style="flex-basis:100%;">
                        <div class="add-breakup">
                        <label for="FirstName">First Name</label>
                        <input type="text" v-model="AddCont.FirstName" class="form-control" id="FirstName" placeholder="First Name">
                        <label for="MiddleName">Middle Name</label>
                        <input type="text" v-model="AddCont.MiddleName" class="form-control" id="MiddleName" placeholder="Middle Name">
                        <label for="LastName">Last Name</label>
                        <input type="text" v-model="AddCont.LastName" class="form-control" id="LastName" placeholder="Last Name">
                        </div>
                        <div class="add-breakup">
                        <label for="WorkPhone">Work Phone</label>
                        <input type="text" v-model="AddCont.WorkPhone" class="form-control" id="WorkPhone" placeholder="Work Phone">
                        <label for="HomePhone">Home Phone</label>
                        <input type="text" v-model="AddCont.HomePhone" class="form-control" id="HomePhone" placeholder="Home Phone">
                        <label for="MobilePhone">Mobile Phone</label>
                        <input type="text" v-model="AddCont.MobilePhone" class="form-control" id="MobilePhone" placeholder="Mobile Phone">
                        </div>
                        <div class="add-breakup">
                        <label for="Email">Email</label>
                        <input type="text" v-model="AddCont.Email" class="form-control" id="Email" placeholder="Email">
                        <label for="URL">URL</label>
                        <input type="text" v-model="AddCont.URL" class="form-control" id="URL" placeholder="URL">
                        <label for="Description">Description</label>
                        <input type="text" v-model="AddCont.Description" class="form-control" id="Description" placeholder="Description">
                        </div>
                        <div class="add-breakup">
                        <label for="Title">Time Zone</label>
                        <input type="text" id="Title" v-model="AddCont.Title" class="form-control" placeholder="Title"/>
                        <label for="TimeZone">Time Zone</label>
                        <input type="text" v-model="AddCont.ContactTimezone" class="form-control" id="TimeZone" placeholder="Time Zone">
                        <label for="Type">Contact Type</label>
                        <b-form-select size="sm" id="Type" :options="consts.CHOICE_FIELDS.Contact.ContactType" v-model="AddCont.ContactType" />
                        <label for="pcm">Preferred Contact Method</label>
                        <b-form-select size="sm" id="Type" :options="consts.CHOICE_FIELDS.Contact.PreferredContactMethod" v-model="AddCont.PreferredContactMethod" />
                        </div>
                        <div style="flex-basis: 100%;margin-bottom:50px;"/>
                        <div class="add-breakup">
                        <label for="Line1">Address Line 1</label>
                        <input type="text" v-model="Address.AddrLine1" class="form-control" id="Line1" placeholder="Line 1">
                        <label for="Line2">Address Line 2</label>
                        <input type="text" v-model="Address.AddrLine2" class="form-control" id="Line2" placeholder="Line 2">
                        <label for="Line3">Address Line 3</label>
                        <input type="text" v-model="Address.AddrLine3" class="form-control" id="Line3" placeholder="Line 3">
                        </div>
                        <div class="add-breakup">
                        <label for="city">City</label>
                        <input type="text" v-model="Address.City" class="form-control" id="city" placeholder="City">
                        <label for="county">County</label>
                        <input type="text" v-model="Address.County" class="form-control" id="county" placeholder="County">
                        <label for="s/p">State/Province</label>
                        <input type="text" v-model="Address.StateProvince" class="form-control" id="s/p" placeholder="State/Province">
                        <label for="country">Country</label>
                        <input type="text" v-model="Address.Country" class="form-control" id="country" placeholder="Country">
                        </div>
                        <div class="add-breakup">
                        <label for="zip">ZIP Code</label>
                        <input type="text" v-model="Address.ZipPostalCode" class="form-control" id="zip" placeholder="ZIP Code">
                        <label for="addrtype">Address Type</label>
                         <b-form-select size="sm" id="addrtype" :options="consts.CHOICE_FIELDS.Address.AddressType" v-model="Address.AddressType" />
                        <label for="Description">Description</label>
                        <input type="text" v-model="Address.Description" class="form-control" id="Description" placeholder="Description">
                        </div>
                        <div class="add-breakup">
                        <label for="locdesc">Location Description</label>
                        <input type="text" v-model="Location.Description" class="form-control" id="locdesc" placeholder="Location Description" />
                        <label for="detmeth">Location Determination Method</label>
                         <b-form-select size="sm" id="detmeth" :options="consts.CHOICE_FIELDS.Location.LocationDeterminationMethod" v-model="Location.LocationDeterminationMethod" />
                         <label for="loctype">Location Type</label>
                         <b-form-select size="sm" id="loctype" :options="consts.CHOICE_FIELDS.Location.LocationType" v-model="Location.LocationType" />
                        </div>
                        <div style="flex-basis:100%;margin-top:25px;"/>
                        <div class="edit-buttons">
                            <a style="margin:0;padding:0;text-decoration: underline;margin-right:10px;" v-on:click="addInspectionCont()">{{(this.replacingInspCont == -1) ?  "Add Contact" : "Save Contact"}}</a>
                        </div>
                    </div>
                    <div style="margin:2px;margin-top:15px;flex-basis:100%;">Created Contacts</div>
                    <div style="margin:2px;margin-top:0px;margin-bottom:25px;border-bottom:1px solid black;height:0px;flex-basis:100%;"></div>
                    <div style="display: flex; align-items:center; flex-direction:column;">
                        <!-- Display contacts added to current inspection -->
                        <div style="display:flex; justify-content:space-between;background-color: white; width:900px;" v-for="(add,index) in AddInsp.Contacts" 
                                        v-bind:key="`addctoaddi-${index}`">
                            <h3>You have added a Contact: {{add.FirstName}}</h3>
                            <!-- Remove this contact from current inspection -->
                            <i v-on:click="deleteInspectionCont(index)" class="fas fa-minus"></i>
                            <!-- Change the data in this contact -->
                            <i v-on:click="returnInspectionCont(index)" class="fas fa-pencil-alt"></i>
                        </div>
                    </div>
                    <!-- Display data from added inspeciton -->
                    <div style="margin:2px;margin-top:15px;flex-basis:100%;">Created Inspections</div>
                    <div style="margin:2px;margin-top:0px;margin-bottom:25px;border-bottom:1px solid black;height:0px;flex-basis:100%;"></div>
                    <div style="display: flex; align-items:center; flex-direction:column;">
                        <div style="display:flex; justify-content:space-between;background-color: white; width:900px;" v-for="(add,index) in inspectionAddition.Value" 
                                        v-bind:key="`addctoaddid-${index}`">
                            <h3>You have added an Inspection: {{add.AHJInspectionName}}</h3>
                            <!-- Remove this inspection from the list -->
                            <i v-on:click="deleteInspectionAddition(index)" class="fas fa-minus"></i>
                            <!-- Edit this inspections information before submitting -->
                            <i v-on:click="returnInspectionAddition(index)" class="fas fa-pencil-alt"></i>
                        </div>
                    </div>
                </div>
                <div class="edit-buttons">
                    <!-- Add this inspection + contacts to list of inspection additions -->
                    <a style="margin:0;padding:0;text-decoration: underline;margin-right:10px;" v-on:click="addInspection()">{{(this.replacingInsp == -1) ?  "Add" : "Save"}}</a>
                    <!-- Close window without adding inspection -->
                    <a style="margin:0;padding:0;text-decoration: underline;" v-on:click="replacingCont=-1;showBigDiv('addainspection')">Cancel</a>
                </div>
            </div>
        </div>
        <!-- Add a document submission method -->
        <div id='addadsub' class='edits hide'>
        <div style="width:15px;height:15px;top:0px;float:right;position:sticky;color:red;" v-on:click="showBigDiv('addadsub')" class="fas fa-times"></div>
        <div class="big-div">
            <div style="margin:2px;">Add a Document Submission Method</div>
            <div style="margin:2px;margin-top:0px;margin-bottom:25px;border-bottom:1px solid black;height:0px;"/>
            <div class="add-breakup">
                <div class="add-cont">
                    <!-- Fields necessary to add a DSM -->
            <label for="dsm">Document Submission Method</label>
            <b-form-select size="sm" id="Type" :options="consts.CHOICE_FIELDS.DocumentSubmissionMethod.DocumentSubmissionMethod" v-model="DSM" />
            </div>
            </div>
            <div style="margin:2px;margin-top:15px;flex-basis:100%;">Created Document Submission Method</div>
            <div style="margin:2px;margin-top:0px;margin-bottom:25px;border-bottom:1px solid black;height:0px;flex-basis:100%;"></div>
            <div style="display: flex; align-items:center; flex-direction:column;">
                <!-- Display added DSM -->
            <div style="display:flex; justify-content:space-between;background-color: white; width:900px;" v-for="(add,index) in AddDSM.Value" 
                                        v-bind:key="`adddsm-${index}`">
                            <h3>You have added a DSM: {{add.Value}}</h3>
                            <!-- Remove DSM deletion, we do not support DSM editing in post -->
                            <i v-on:click="deleteDSMAddition(index)" class="fas fa-minus"></i>
                        </div>
                        </div>
            <div class="edit-buttons">
                <!-- Add DSM to additions list -->
                    <a style="margin:0;padding:0;text-decoration: underline;margin-right:10px;" v-on:click="addDSM()">Add</a>
                    <!-- Close window without adding DSM to additions list -->
                    <a style="margin:0;padding:0;text-decoration: underline;" v-on:click="showBigDiv('addadsub')">Cancel</a>
            </div>
        </div>
        </div>
        <!-- Window to add a permit issue method -->
        <div id='addapermitissue' class='edits hide'>
        <div style="width:15px;height:15px;top:0px;float:right;position:sticky;color:red;" v-on:click="showBigDiv('addapermitissue')" class="fas fa-times"></div>
        <div class="big-div">
            <div style="margin:2px;">Add a Permit Issue Method</div>
            <div style="margin:2px;margin-top:0px;margin-bottom:25px;border-bottom:1px solid black;height:0px;"/>
            <div class="add-breakup">
                <div class="add-cont">
            <label for="dsm">Permit Issue Method</label>
            <!-- Field needed for a PIM -->
            <b-form-select size="sm" id="Type" :options="consts.CHOICE_FIELDS.PermitIssueMethod.PermitIssueMethod" v-model="PIM" />
            </div>
            </div>
            <!-- Display created permit issue methods -->
            <div style="margin:2px;margin-top:15px;flex-basis:100%;">Created Permit Issue Method</div>
            <div style="margin:2px;margin-top:0px;margin-bottom:25px;border-bottom:1px solid black;height:0px;flex-basis:100%;"></div>
            <div style="display: flex; align-items:center; flex-direction:column;">
            <div style="display:flex; justify-content:space-between;background-color: white; width:900px;" v-for="(add,index) in AddPIM.Value" 
                                        v-bind:key="`addedPIM${index}`">
                            <h3>You have added a PIM: {{add.Value}}</h3>
                            <!-- Delete a PIM Additions, we do not support editing PIM in Post -->
                            <i v-on:click="deletePIMAddition(index)" class="fas fa-minus"></i>
                        </div>
                        </div>
            <div class="edit-buttons">
                <!-- Add to list of PIM Additions -->
                    <a style="margin:0;padding:0;text-decoration: underline;margin-right:10px;" v-on:click="addPIM()">Add</a>
                    <!-- Close window without adding PIM to Additions list --> 
                    <a style="margin:0;padding:0;text-decoration: underline;" v-on:click="showBigDiv('addapermitissue')">Cancel</a>
            </div>
        </div>
        </div>
        <!-- Window to add an Engineering Review Requirement -->
        <div id="addaerr" class="edits hide">
            <div style="width:15px;height:15px;top:0px;float:right;position:sticky;color:red;" v-on:click="showBigDiv('addaerr')" class="fas fa-times"></div>
            <div class="big-div">
                <div style="margin:2px;">Add an Engineering Review Requirement</div>
                <div style="margin:2px;margin-top:0px;margin-bottom:25px;border-bottom:1px solid black;height:0px;"/>
                <div class="add-cont">
                    <!-- Fields necessary for an ERR as text entry boxes -->
                    <div class="add-breakup">
                        <label for="errtype">Engineering Review Type</label>
                        <b-form-select size="sm" id="errtype" v-model="AddERR.EngineeringReviewType" :options="consts.CHOICE_FIELDS.EngineeringReviewRequirement.EngineeringReviewType"/>
                        <label for="rlevel">Requirement Level</label>
                        <b-form-select size="sm" id="rlevel" v-model="AddERR.RequirementLevel" :options="consts.CHOICE_FIELDS.EngineeringReviewRequirement.RequirementLevel"/>
                        <label for="rnotes">Requirement Notes</label>
                        <input  type="text" v-model="AddERR.RequirementNotes" />
                    </div>
                    <div class="add-breakup">
                        <label for="stamptype">Stamp Type</label>
                        <b-form-select size="sm" id="stamptype" v-model="AddERR.StampType" :options="consts.CHOICE_FIELDS.EngineeringReviewRequirement.StampType"/>
                        <label for="desc-err">Description</label>
                        <textarea v-model="AddERR.Description"/>
                    </div>
                </div>
                <!-- Display all created ERR -->
                <div style="margin:2px;margin-top:15px;flex-basis:100%;">Created Engineering Review Requirements</div>
                <div style="margin:2px;margin-top:0px;margin-bottom:25px;border-bottom:1px solid black;height:0px;flex-basis:100%;"></div>
                <div style="display: flex; align-items:center; flex-direction:column;">
                        <div style="display:flex; justify-content:space-between;background-color: white; width:900px;" v-for="(add,index) in ERRAddition.Value" 
                                        v-bind:key="`addederr${index}`">
                                        <h3>You have added an Engineering Review Requirement: {{add.EngineeringReviewType}}</h3>
                                        <!-- Delete ERR addition -->
                            <i v-on:click="deleteERRAddition(index)" class="fas fa-minus"></i>
                            <!-- Allow user to edit previously added ERR -->
                            <i v-on:click="returnERRAddition(index)" class="fas fa-pencil-alt"></i>
                </div>
                </div>
                <div class="edit-buttons">
                    <!-- Add ERR to list of ERR Additions -->
                    <a style="margin:0;padding:0;text-decoration: underline;margin-right:10px;" v-on:click="addERR()">{{(this.replacingERR == -1) ?  "Add" : "Save"}}</a>
                    <!-- Close window without adding ERR to additions list -->
                    <a style="margin:0;padding:0;text-decoration: underline;" v-on:click="showBigDiv('addaerr')">Cancel</a>
            </div>
            </div>
        </div>
        <!-- Window to add a fee structure -->
        <div id="addafstruct" class="edits hide">
            <div style="width:15px;height:15px;top:0px;float:right;position:sticky;color:red;" v-on:click="showBigDiv('addafstruct')" class="fas fa-times"></div>
            <div class="big-div">
                <div style="margin:2px;">Add a Fee Structure</div>
                <div style="margin:2px;margin-top:0px;margin-bottom:25px;border-bottom:1px solid black;height:0px;"/>
                <div class="add-cont">
                    <!-- Fields to add a Fee Structure -->
                    <div class="add-breakup">
                        <label for="fsid">Fee Structure ID</label>
                        <input id="fsid" type="text" v-model="AddFS.FeeStructureID"/>
                        <label for="fsname">Fee Structure Name</label>
                        <input id="fsname" type="text" v-model="AddFS.FeeStructureName" />
                        <label for="fstype">Fee Structure Type</label>
                        <b-form-select size="sm" id="fstype" v-model="AddFS.FeeStructureType" :options="consts.CHOICE_FIELDS.FeeStructure.FeeStructureType"/>
                        <label for="fsdesc">Description</label>
                        <textarea id="fsdesc"/>
                    </div>
                </div>
                <!-- Display created FS -->
                <div style="margin:2px;margin-top:15px;flex-basis:100%;">Created Fee Structures</div>
                <div style="margin:2px;margin-top:0px;margin-bottom:25px;border-bottom:1px solid black;height:0px;flex-basis:100%;"></div>
                <div style="display: flex; align-items:center; flex-direction:column;">
                        <div style="display:flex; justify-content:space-between;background-color: white; width:900px;" v-for="(add,index) in FSAddition.Value" 
                                        v-bind:key="`addedfs${index}`">
                                        <h3>You have added a Fee Structure: {{add.FeeStructureName}}</h3>
                                        <!-- Remove created FS additions -->
                            <i v-on:click="deleteFSAddition(index)" class="fas fa-minus"></i>
                            <!-- Allow user to edit FS additions -->
                            <i v-on:click="returnFSAddition(index)" class="fas fa-pencil-alt"></i>
                </div>
                </div>
                <div class="edit-buttons">
                    <!-- Add FS to additions list -->
                    <a style="margin:0;padding:0;text-decoration: underline;margin-right:10px;" v-on:click="addFS()">{{(this.replacingFS == -1) ?  "Add" : "Save"}}</a>
                    <!-- Close window without adding FS to created list -->
                    <a style="margin:0;padding:0;text-decoration: underline;" v-on:click="showBigDiv('addafstruct')">Cancel</a>
            </div>
            </div>
        </div>
        <div id="addressLoc" class="edits hide">
            <div style="width:15px;height:15px;top:0px;float:right;position:sticky;color:red;" v-on:click="showBigDiv('addressLoc')" class="fas fa-times"></div>
            <div class="big-div">
                <div class="edit-title">Edit Address</div>
                <div class="add-cont" style="flex-basis:100%;">
                <div style="flex-basis: 100%;margin-bottom:50px;"/>
                        <div class="add-breakup">
                        <label for="Line1">Address Line 1</label>
                        <input type="text" v-model="Address.AddrLine1" class="form-control" id="Line1" placeholder="Line 1">
                        <label for="Line2">Address Line 2</label>
                        <input type="text" v-model="Address.AddrLine2" class="form-control" id="Line2" placeholder="Line 2">
                        <label for="Line3">Address Line 3</label>
                        <input type="text" v-model="Address.AddrLine3" class="form-control" id="Line3" placeholder="Line 3">
                        </div>
                        <div class="add-breakup">
                        <label for="city">City</label>
                        <input type="text" v-model="Address.City" class="form-control" id="city" placeholder="City">
                        <label for="county">County</label>
                        <input type="text" v-model="Address.County" class="form-control" id="county" placeholder="County">
                        <label for="s/p">State/Province</label>
                        <input type="text" v-model="Address.StateProvince" class="form-control" id="s/p" placeholder="State/Province">
                        <label for="country">Country</label>
                        <input type="text" v-model="Address.Country" class="form-control" id="country" placeholder="Country">
                        </div>
                        <div class="add-breakup">
                        <label for="zip">ZIP Code</label>
                        <input type="text" v-model="Address.ZipPostalCode" class="form-control" id="zip" placeholder="ZIP Code">
                        <label for="addrtype">Address Type</label>
                         <b-form-select size="sm" id="addrtype" :options="consts.CHOICE_FIELDS.Address.AddressType" v-model="Address.AddressType" />
                        <label for="Description">Description</label>
                        <input type="text" v-model="Address.Description" class="form-control" id="Description" placeholder="Description">
                        </div>
                        <div class="add-breakup">
                        <label for="locdesc">Location Description</label>
                        <input type="text" v-model="Location.Description" class="form-control" id="locdesc" placeholder="Location Description" />
                        <label for="detmeth">Location Determination Method</label>
                         <b-form-select size="sm" id="detmeth" :options="consts.CHOICE_FIELDS.Location.LocationDeterminationMethod" v-model="Location.LocationDeterminationMethod" />
                         <label for="loctype">Location Type</label>
                         <b-form-select size="sm" id="loctype" :options="consts.CHOICE_FIELDS.Location.LocationType" v-model="Location.LocationType" />
                        </div>
                        </div>
                        <div class="edit-buttons">
                            <!-- Adds contact to list of current contacts -->
                            <a style="margin:0;padding:0;text-decoration: underline;margin-right:10px;" v-on:click="editAddress()">{{(this.editingCont == -1) ?  "Add" : "Save"}}</a>
                            <!-- Closes the window without adding contact to list -->
                            <a style="margin:0;padding:0;text-decoration: underline;" v-on:click="clearAddrAndLocation();showBigDiv('addressLoc');editingCont = -1">Cancel</a>
                        </div>
            </div>
        </div>
        <!-- Window to display edits that were already submitted, i.e. Coming from the backend (see EditObject.vue) -->
        <div id="edits" class='edits hide'>
            <div style="width:15px;height:15px;top:0px;float:right;position:sticky;color:red;" v-on:click="showBigDiv('edits')" class="fas fa-times"></div>
            <div id="mid-edits" class='big-div'>
                <div class="edit-title">AHJ</div>
                <div id="Address-edits" class="edit-body">
                    <div v-for="(e,index) in editList" v-bind:key="`ahjedit${index}`">
                        <div v-if="baseFields.has(e.SourceColumn)">
                            <edit-object v-bind:data="e" v-on:official="handleOfficial($event)"/>
                        </div>
                    </div>
                </div>
                <div class="edit-title">Address</div>
                <div id="Address-edits" class="edit-body">
                    <div v-for="(e,index) in editList" v-bind:key="`addredit${index}`">
                        <div v-if="AHJInfo && (e.SourceTable==='Address' && e.SourceRow==AHJInfo.Address.AddressID.Value) || (e.SourceTable==='Location' && e.SourceRow == AHJInfo.Address.Location.LocationID)">
                            <edit-object v-bind:data="e" v-on:official="handleOfficial($event)"/>
                        </div>
                    </div>
                </div>
                <!-- Loop through building Code edits and display -->
                <div class="edit-title">Building Codes</div>
                <div id="BuildingCode-edits" class="edit-body">
                    <div v-for="(e,index) in editList" v-bind:key="`bcnot${index}`">
                        <div v-if="e.SourceColumn === 'BuildingCode'">
                            <edit-object v-bind:data="e" v-on:official="handleOfficial($event)"/>
                        </div>
                    </div>
                </div>
                <!-- Loop through building code notes edits and display -->
                <div class="edit-title">Building Code Notes</div>
                <div id="BuildingCodeNotes-edits" class="edit-body">
                    <div v-for="(e,index) in editList" v-bind:key="`bcnotes${index}`">
                        <div v-if="e.SourceColumn === 'BuildingCodeNotes'">
                            <edit-object v-bind:data="e" v-on:official="handleOfficial($event)"/>
                        </div>
                    </div>
                </div>
                <!-- Loop through Electric Code edits -->
                <div class="edit-title">Electrical Codes</div>
                <div id="ElectricCode-edits" class="edit-body">
                    <div v-for="(e,index) in editList" v-bind:key="`ecnot${index}`">
                        <div v-if="e.SourceColumn === 'ElectricCode'">
                            <edit-object v-bind:data="e" v-on:official="handleOfficial($event)"/>
                        </div>
                    </div>
                </div>
                <!-- Loop through Electric Code notes edits -->
                <div class="edit-title">Electrical Code Notes</div>
                <div class="edit-body">
                    <div v-for="(e,index) in editList" v-bind:key="`ecnotes${index}`">
                        <div v-if="e.SourceColumn === 'ElectricCodeNotes'">
                            <edit-object v-bind:data="e" v-on:official="handleOfficial($event)"/>
                        </div>
                    </div>
                </div>
                <!-- Loop through and display Fire code edit -->
                <div class="edit-title">Fire Codes</div>
                <div id="FireCode-edits" class="edit-body">
                    <div v-for="(e,index) in editList" v-bind:key="`fcnot${index}`">
                        <div v-if="e.SourceColumn === 'FireCode'">
                            <edit-object v-bind:data="e" v-on:official="handleOfficial($event)"/>
                        </div>
                    </div>
                </div>
                <!-- Loop through and display Fire Code Notes edits -->
                 <div class="edit-title">Fire Code Notes</div>
                <div class="edit-body">
                    <div v-for="(e,index) in editList" v-bind:key="`fcnotes${index}`">
                        <div v-if="e.SourceColumn === 'FireCodeNotes'">
                            <edit-object v-bind:data="e" v-on:official="handleOfficial($event)"/>
                        </div>
                    </div>
                </div>
                <!-- Loop through and display residential code edits -->
                <div class="edit-title">Residential Codes</div>
                <div id="ResidentialCode-edits" class="edit-body">
                    <div v-for="(e,index) in editList" v-bind:key="`rcnot${index}`">
                        <div v-if="e.SourceColumn === 'ResidentialCode'">
                            <edit-object v-bind:data="e" v-on:official="handleOfficial($event)"/>
                        </div>
                    </div>
                </div>
                <!-- Loop through and display Residential code Notes edits -->
                 <div class="edit-title">Residential Code Notes</div>
                <div class="edit-body">
                    <div v-for="(e,index) in editList" v-bind:key="`rcnotes${index}`">
                        <div v-if="e.SourceColumn === 'ResidentialCodeNotes'">
                            <edit-object v-bind:data="e" v-on:official="handleOfficial($event)"/>
                        </div>
                    </div>
                </div>
                <!-- Loop through and display wind code edits -->
                <div class="edit-title">Wind Codes</div>
                <div id="WindCode-edits" class="edit-body">
                    <div v-for="(e,index) in editList" v-bind:key="`wcnot${index}`">
                        <div v-if="e.SourceColumn === 'WindCode'">
                            <edit-object v-bind:data="e" v-on:official="handleOfficial($event)"/>
                        </div>
                    </div>
                </div>
                <!-- Loop through and display Wind Code Notes Edit -->
                 <div class="edit-title">Wind Code Notes</div>
                <div class="edit-body">
                    <div v-for="(e,index) in editList" v-bind:key="`wcnotes${index}`">
                        <div v-if="e.SourceColumn === 'WindCodeNotes'">
                            <edit-object v-bind:data="e" v-on:official="handleOfficial($event)"/>
                        </div>
                    </div>
                </div>
                <!-- Edits on contacts -->
                <div class="edit-title">Contacts</div>
                <div class="edit-body">
                    <div v-if="AHJInfo != null">
                        <!-- Loop through each contact on this AHJ -->
                    <div v-for="(c,index) in AHJInfo.Contacts" v-bind:key="`c-${index}`">
                        <div class="edit-title">{{c.FirstName.Value + " " + c.LastName.Value}}</div>
                        <div class="edit-body no-border">
                            <!-- Loop through the edits made on this AHJ and find the ones that were made on this contact, i.e. edit.ContactID and contact.ContactID match -->
                        <div v-for="(e,index) in editList" v-bind:key="`c-e-${index}`">
                            <edit-object v-if="e.SourceTable==='Contact' && e.SourceRow===c.ContactID.Value && e.EditType==='U'" v-bind:data="e" v-on:official="handleOfficial($event)"/>
                            <edit-object v-if="(e.SourceTable==='Address' && e.SourceRow==c.Address.AddressID.Value) || (e.SourceTable==='Location' && e.SourceRow==c.Address.Location.LocationID.Value)"
                            v-bind:data="e" v-on:official="handleOfficial($event)"/>
                        </div>
                        </div>
                    </div>
                    <div class="edit-title">Contact Additions</div>
                    <div class="edit-body no-border">
                        <!-- Loop through all edits made on this AHJ -->
                    <div v-for="e in editList" v-bind:key="`c-e-a-${e.EditID}`">
                        <!-- Loop through both confirmed and unconfirmed contacts on this AHJ to find the one associated with this edit -->
                        <div v-for="c in allContacts" v-bind:key="`c-a-${c.ContactID.Value}`">
                            <div v-if="e.SourceRow==c.ContactID.Value && e.SourceTable==='Contact' && e.EditType==='A'">
                                <contact-card v-bind:data="c" v-bind:eID="e.EditID" v-on:official="handleOfficial($event)" v-bind:editStatus="e.ReviewStatus"/>
                            </div>
                        </div>
                    </div>
                    </div>
                    <div class="edit-title">Contact Deletions</div>
                    <div class="edit-body no-border">
                        <!-- Loop through all edits on this AHJ -->
                    <div v-for="e in editList" v-bind:key="`c-d-${e.EditID}`">
                        <!-- Loop through both confirmed and unconfirmed contacts on this AHJ to find the one associated with this edit -->
                        <div v-for="c in allContacts" v-bind:key="`c-d-${c.ContactID.Value}`">
                            <div v-if="e.SourceRow==c.ContactID.Value && e.SourceTable==='Contact' && e.EditType==='D'">
                                <contact-card v-bind:data="c" v-bind:eID="e.EditID" v-on:official="handleOfficial($event)" v-bind:editStatus="e.ReviewStatus"/>
                            </div>
                        </div>
                    </div>
                    </div>
                    </div>
                    <div style="margin-bottom:25px;"/>
                </div>
                <!-- Edits on Inspections -->
                <div class="edit-title">Inspections</div>
                <div class="edit-body">
                    <div v-if="AHJInfo != null">
                        <!-- Loop through confirmed inspections on this AHJ -->
                    <div v-for="(c,index) in AHJInfo.AHJInspections" v-bind:key="`i-${index}`">
                        <div class="edit-title">{{c.AHJInspectionName.Value}}</div>
                        <!-- Loop through all edits and find the ones associated with this Inspection -->
                        <div v-for="(e,index) in editList" v-bind:key="`i-e-${index}`">
                            <edit-object v-if="e.SourceTable==='AHJInspection' && e.SourceRow===c.InspectionID.Value  && e.EditType==='U'" v-bind:data="e" v-on:official="handleOfficial($event)"/>
                        </div>
                        <div class="edit-body no-border">
                            <!-- Loop through all the contacts for this inspection -->
                            <div v-for="(ci,index) in c.Contacts" v-bind:key="`i-c-${index}`">
                                <div class="edit-title">{{ci.FirstName.Value + " " + ci.LastName.Value}}</div>
                                <!-- Loop throught edits and find the ones associated with this contact -->
                                <div v-for="(e,index) in editList" v-bind:key="`i-c-e-${index}`">
                                    <edit-object v-if="e.SourceTable==='Contact' && e.SourceRow===ci.ContactID.Value && e.EditType==='U'" v-bind:data="e" v-on:official="handleOfficial($event)"/>
                                </div>
                            </div>
                        </div>
                        <!-- Contacts added to this inspection -->
                        <div class="edit-title">Contact Additions</div>
                        <div class="edit-body no-border">
                            <!-- Loop through edit list -->
                            <div v-for="e in editList" v-bind:key="`i-c-a-e-${e.EditID}`">
                                <!-- Find unconfirmed contact associated with edits and display -->
                                <div v-for="ic in c.UnconfirmedContacts" v-bind:key="`i-c-a-${ic.ContactID.Value}`">
                                    <contact-card v-bind:editStatus="e.ReviewStatus" v-if="e.SourceTable==='Contact' && e.SourceRow == ic.ContactID.Value && e.EditType==='A'" v-bind:data="ic" v-bind:eID="e.EditID" v-on:official="handleOfficial($event)"/>
                                </div>
                            </div>
                            <!-- Loop through Edit list -->
                            <div v-for="e in editList" v-bind:key="`i-c-a-e-u${e.EditID}`">
                                <!-- Find confirmed contacts associated with edits -->
                                <div v-for="ic in c.Contacts" v-bind:key="`i-c-a-u-${ic.ContactID.Value}`">
                                    <contact-card v-bind:editStatus="e.ReviewStatus" v-if="e.SourceTable==='Contact' && e.SourceRow == ic.ContactID.Value && e.EditType==='A'" v-bind:data="ic" v-bind:eID="e.EditID" v-on:official="handleOfficial($event)"/>
                                </div>
                            </div>
                        </div>
                        <!-- Contacts Deleted from this inspection -->
                        <div class="edit-title">Contact Deletions</div>
                        <div class="edit-body no-border">
                            <!-- Loop through edit List -->
                            <div v-for="e in editList" v-bind:key="`i-c-e-d-${e.EditID}`">
                                <!-- Find unconfirmed contacts associated with edits and display -->
                                <div v-for="ic in c.UnconfirmedContacts" v-bind:key="`i-c-d-${ic.ContactID.Value}`">
                                    <div v-if="e.SourceTable==='Contact' && e.SourceRow == ic.ContactID.Value && e.EditType==='D'">
                                        <contact-card v-bind:editStatus="e.ReviewStatus" v-if="e.SourceTable==='Contact' && e.SourceRow == ic.ContactID.Value && e.EditType==='D'" v-bind:data="ic" v-bind:eID="e.EditID" v-on:official="handleOfficial($event)"/>
                                    </div>
                                </div>
                            </div>
                            <!-- Loop through edit list -->
                            <div v-for="e in editList" v-bind:key="`i-c-e-d-u${e.EditID}`">
                                <!-- Find confirmed contacts associated with edit and display -->
                                <div v-for="ic in c.Contacts" v-bind:key="`i-c-d-u-${ic.ContactID.Value}`">
                                    <div v-if="e.SourceTable==='Contact' && e.SourceRow == ic.ContactID.Value && e.EditType==='D'">
                                        <contact-card v-bind:editStatus="e.ReviewStatus" v-if="e.SourceTable==='Contact' && e.SourceRow == ic.ContactID.Value && e.EditType==='D'" v-bind:data="ic" v-bind:eID="e.EditID" v-on:official="handleOfficial($event)"/>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <!-- Inspections addded to this AHJ -->
                    <div class="edit-title">Inspection Additions</div>
                    <div class="edit-body no-border">
                        <!-- Loop through eddit list -->
                    <div v-for="e in editList" v-bind:key="`i-a-e-${e.EditID}`">
                        <!-- Find inspection associated with edit and display -->
                        <div v-for="c in allInspections" v-bind:key="`i-a-c-${c.InspectionID.Value}`">
                            <div v-if="e.SourceRow===c.InspectionID.Value && e.SourceTable==='AHJInspection' && e.EditType==='A'">
                                <inspection v-bind:editStatus="e.ReviewStatus" v-bind:data="c" v-bind:eID="e.EditID" v-on:official="handleOfficial($event)"/>
                            </div>
                        </div>
                    </div>
                    </div>
                    <!-- Inspections deleted from this AHJ -->
                    <div class="edit-title">Inspection Deletions</div>
                    <div class="edit-body no-border">
                        <!-- Loop through edits -->
                    <div v-for="e in editList" v-bind:key="`i-d-e-${e.EditID}`">
                        <!-- Find inspection associated with edit and display -->
                        <div v-for="c in allInspections" v-bind:key="`i-d-c-${c.InspectionID.Value}`">
                            <div v-if="e.SourceRow==c.InspectionID.Value && e.SourceTable==='AHJInspection' && e.EditType==='D'">
                                <inspection v-bind:editStatus="e.ReviewStatus" v-bind:data="c" v-bind:eID="e.EditID" v-on:official="handleOfficial($event)"/>
                            </div>
                        </div>
                    </div>
                    </div>
                    </div>
                    <div style="margin-bottom:25px;"/>
                </div>
                <!-- Document submission method edits -->
                <div class="edit-title">Document Submission Methods</div>
                <div class="edit-body">
                    <!-- DSM Additions to this AHJ -->
                    <div class="edit-title">Additions</div>
                    <div class="edit-body no-border">
                        <!-- Loop through edits -->
                        <div v-for="e in editList" v-bind:key="`DSM-e-a-${e.EditID}`">
                            <div v-if="e.SourceTable ==='AHJDocumentSubmissionMethodUse'">
                            <div v-for="err in allDSM" v-bind:key="`DSM-a-${err.UseID}`">
                                <div v-if="e.SourceRow == err.UseID && e.EditType==='A'">
                                <h2 :ref="`DSM-a-${err.UseID}`" v-bind:style="{backgroundColor: e.ReviewStatus==='A' ? '#B7FFB3' : e.ReviewStatus==='R' ? '#FFBEBE' : 'white'}"  class="pmdsm"> {{err.Value}} </h2>
                                <i style="margin-right:10px" v-if="isManaged && e.ReviewStatus==='P'" v-on:click="handleOfficial({Type:'Accept',eID:e.EditID});e.ReviewStatus = 'A';changeStatus(`DSM-a-${err.UseID}`,'A');" class="fa fa-check"></i>
                                <i v-if="isManaged && e.ReviewStatus==='P'" v-on:click="handleOfficial({Type:'Reject',eID:e.EditID});e.ReviewStatus='R';changeStatus(`DSM-a-${err.UseID}`,'R');" class="fa fa-thumbs-down"></i>
                                </div>
                            </div>
                            </div>
                        </div>
                    </div>
                    <!-- DSM Deletions on this AHJ -->
                    <div class="edit-title">Deletions</div>
                    <div class="edit-body no-border">
                        <!-- Loop through edit list -->
                        <div v-for="e in editList" v-bind:key="`DSM-e-d-${e.EditID}`">
                            <div v-if="e.SourceTable ==='AHJDocumentSubmissionMethodUse'">
                            <div v-for="err in allDSM" v-bind:key="`DSM-d-${err.UseID}`">
                                <div v-if="e.SourceRow == err.UseID && e.EditType==='D'">
                                <h2 :ref="`DSM-a-${err.UseID}`" v-bind:style="{backgroundColor: e.ReviewStatus==='A' ? '#B7FFB3' : e.ReviewStatus==='R' ? '#FFBEBE' : 'white'}"  class="pmdsm"> {{err.Value}} </h2>
                                <i style="margin-right:10px" v-if="isManaged && e.ReviewStatus==='P'" v-on:click="handleOfficial({Type:'Accept',eID:e.EditID});e.ReviewStatus = 'A';changeStatus(`DSM-a-${err.UseID}`,'A');" class="fa fa-check"></i>
                                <i v-if="isManaged && e.ReviewStatus==='P'" v-on:click="handleOfficial({Type:'Reject',eID:e.EditID});e.ReviewStatus='R';changeStatus(`DSM-a-${err.UseID}`,'R');" class="fa fa-thumbs-down"></i>
                                </div>
                            </div>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- Engineering review requirement edits -->
                <div class="edit-title">Engineering Review Requirements</div>
                <div class="edit-body">
                    <div v-if="AHJInfo !== null">
                        <!-- Loop through all ERR -->
                    <div v-for="err in AHJInfo.EngineeringReviewRequirements" v-bind:key="`err-${err.EngineeringReviewRequirementID.Value}`">
                        <div class="edit-title">{{err.EngineeringReviewType.Value}}</div>
                        <!-- Loop through edits and find ones associated with each ERR and display -->
                        <div v-for="e in editList" v-bind:key="`err-e-${e.EditID}`">
                            <edit-object v-if="e.SourceRow == err.EngineeringReviewRequirementID && e.SourceTable === 'EngineeringReviewRequirement'  && e.EditType==='U'" v-bind:data="e" v-on:official="handleOfficial($event)"/>
                        </div>
                    </div>
                    </div>
                    <!-- ERR additions -->
                    <div class="edit-title">Additions</div>
                    <div class="edit-body no-border">
                        <!--Loop through edit list -->
                        <div v-for="e in editList" v-bind:key="`err-e-a-${e.EditID}`">
                            <!-- Find ERR associated with edits and display -->
                            <div v-for="err in allERR" v-bind:key="`err-a-${err.EngineeringReviewRequirementID.Value}`">
                                <err-card v-bind:editStatus="e.ReviewStatus" v-if="e.SourceTable === 'EngineeringReviewRequirement' && e.SourceRow == err.EngineeringReviewRequirementID.Value && e.EditType==='A'" v-bind:data="err" v-bind:eID="e.EditID" v-on:official="handleOfficial($event)"/>
                            </div>
                        </div>
                    </div>
                    <!-- ERR Deletions  -->
                    <div class="edit-title">Deletions</div>
                    <div class="edit-body no-border">
                        <!-- Loop through edits -->
                        <div v-for="e in editList" v-bind:key="`err-e-d-${e.EditID}`">
                            <!-- Find ERR associated with this edit and display -->
                            <div v-for="err in allERR" v-bind:key="`err-d-${err.EngineeringReviewRequirementID.Value}`">
                                <err-card v-bind:editStatus="e.ReviewStatus" v-if="e.SourceTable === 'EngineeringReviewRequirement' && e.SourceRow == err.EngineeringReviewRequirementID.Value && e.EditType==='D'" v-bind:data="err" v-bind:eID="e.EditID" v-on:official="handleOfficial($event)"/>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- Fee Structure Edits -->
                <div class="edit-title">Fee Structures</div>
                <div class="edit-body">
                   <div v-if="AHJInfo !== null">
                       <!-- Loop through Fee Structures -->
                    <div v-for="err in AHJInfo.FeeStructures" v-bind:key="`fs-${err.FeeStructurePK.Value}`">
                        <div class="edit-title">{{err.FeeStructureName.Value}}</div>
                        <!-- Find edits associated with each Fee Structure and display -->
                        <div v-for="e in editList" v-bind:key="`fs-e-${e.EditID}`">
                            <edit-object v-if="e.SourceRow == err.FeeStructurePK.Value && e.SourceTable === 'FeeStructure'  && e.EditType==='U'" v-bind:data="e" v-on:official="handleOfficial($event)"/>
                        </div>
                    </div>
                    </div>
                    <!-- FS Additions -->
                    <div class="edit-title">Additions</div>
                    <div class="edit-body no-border">
                        <!-- Loop through edits -->
                        <div v-for="e in editList" v-bind:key="`fs-e-a-${e.EditID}`">
                            <!-- Find FS Associated with each addition edit and display -->
                            <div v-for="err in allFS" v-bind:key="`fs-a-${err.FeeStructurePK.Value}`">
                                <fs-card v-bind:editStatus="e.ReviewStatus" v-if="e.SourceTable === 'FeeStructure' && e.SourceRow == err.FeeStructurePK.Value && e.EditType==='A'" v-bind:data="err" v-bind:eID="e.EditID" v-on:official="handleOfficial($event)"/>
                            </div>
                        </div>
                    </div>
                    <!-- FS Deletions -->
                    <div class="edit-title">Deletions</div>
                    <div class="edit-body no-border">
                        <!-- Loop through edits -->
                        <div v-for="e in editList" v-bind:key="`fs-d-e-${e.EditID}`">
                            <!-- Loop through all FS and find ones associated with Edits -->
                            <div v-for="err in allFS" v-bind:key="`fs-d-${err.FeeStructurePK.Value}`">
                                <fs-card v-bind:editStatus="e.ReviewStatus" v-if="e.SourceTable === 'FeeStructure' && e.SourceRow == err.FeeStructurePK.Value && e.EditType==='D'" v-bind:data="err" v-bind:eID="e.EditID" v-on:official="handleOfficial($event)"/>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- Permit Issue Method edits -->
                <div class="edit-title">Permit Issue Methods</div>
                <div class="edit-body">
                    <!-- PIM Additions -->
                <div class="edit-title">Additions</div>
                    <div class="edit-body no-border">
                        <!-- Loop through edits -->
                        <div v-for="e in editList" v-bind:key="`PIM-${e.EditID}`">
                            <div v-if="e.SourceTable ==='AHJPermitIssueMethodUse'">
                            <div v-for="err in allPIM" v-bind:key="`PIM-e-${err.UseID}`">
                                <div v-if="e.SourceColumn==='MethodStatus' && e.SourceRow == err.UseID && e.EditType==='A'">
                                <h2 :ref="`PIM-e-${err.UseID}`" v-bind:style="{backgroundColor: e.ReviewStatus==='A' ? '#B7FFB3' : e.ReviewStatus==='R' ? '#FFBEBE' : 'white'}"  class="pmdsm"> {{err.Value}} </h2>
                                <i style="margin-right:10px" v-if="isManaged && e.ReviewStatus==='P'" v-on:click="handleOfficial({Type:'Accept',eID:e.EditID});e.ReviewStatus = 'A';changeStatus(`PIM-e-${err.UseID}`,'A');" class="fa fa-check"></i>
                                <i v-if="isManaged && e.ReviewStatus==='P'" v-on:click="handleOfficial({Type:'Reject',eID:e.EditID});e.ReviewStatus='R';changeStatus(`PIM-e-${err.UseID}`,'R');" class="fa fa-thumbs-down"></i>
                                </div>
                            </div>
                            </div>
                        </div>
                    </div>
                    <!-- PIM Deletions -->
                    <div class="edit-title">Deletions</div>
                    <div class="edit-body no-border">
                        <!-- Loop through edits -->
                        <div v-for="e in editList" v-bind:key="`PIM-d-${e.EditID}`">
                            <div v-if="e.SourceTable ==='AHJPermitIssueMethodUse'">
                            <div v-for="err in allPIM" v-bind:key="`PIM-e-d-${err.UseID}`">
                                <div v-if="e.SourceRow == err.UseID && e.EditType==='D'">
                                <h2 :ref="`PIM-e-${err.UseID}`" v-bind:style="{backgroundColor: e.ReviewStatus==='A' ? '#B7FFB3' : e.ReviewStatus==='R' ? '#FFBEBE' : 'white'}"  class="pmdsm"> {{err.Value}} </h2>
                                <i style="margin-right:10px" v-if="isManaged && e.ReviewStatus==='P'" v-on:click="handleOfficial({Type:'Accept',eID:e.EditID});e.ReviewStatus = 'A';changeStatus(`PIM-e-${err.UseID}`,'A');" class="fa fa-check"></i>
                                <i v-if="isManaged && e.ReviewStatus==='P'" v-on:click="handleOfficial({Type:'Reject',eID:e.EditID});e.ReviewStatus='R';changeStatus(`PIM-e-${err.UseID}`,'R');" class="fa fa-thumbs-down"></i>
                                </div>
                            </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div id="make-edits" class='edits hide'>
            <div style="width:15px;height:15px;top:0px;float:right;position:sticky;color:red;" v-on:click="showBigDiv('make-edits')" class="fas fa-times"></div>
            <div id="mid-edits" class='big-div'>
                
            </div>
        </div>
        <!-- Header to page -->
        <div id='titleCard'  ref="titleInfo">
            <div id='mapDiv' ref="map">

            </div>
            <div id='text'>
                <!-- Display name and Value or "Loading" -->
                <h1 id='name'> {{ this.AHJInfo ? this.AHJInfo.AHJName["Value"] : 'Loading' }} </h1>
                <h1 id='code'> {{ this.AHJInfo ? this.AHJInfo.AHJCode.Value : 'Loading' }} </h1>
                <div class="break">
                </div>
                <div v-if="!isEditing" id="addr">
                    <h3> {{this.AddressString}}</h3>
                </div>
                <div style="height:18px" v-else>
                    <a style="margin:0px;padding:0px;text-decoration: underline; cursor:pointer;" v-on:click="setAddrAndLocation();showBigDiv('addressLoc')">Edit this address</a>
                </div>
                <div>
                    <h3>AHJID: {{ this.AHJInfo ? this.AHJInfo.AHJID.Value : 'Loading' }}</h3>
                </div>
                <div class="break"/>
                <div style="height:10px;"/>
                <div class="break"/>
                <div style="position:absolute;right:50%;top:93%;">
                    <h3 v-on:click="toggleMoreInfo()"> <i id="moreInfoChev" class="fa fa-chevron-down"/> More Info</h3>
                </div>
                <div v-if="showMore">
                    <h3 v-if="!isEditing">Description: {{ this.AHJInfo ? this.AHJInfo.Description.Value : 'Loading' }}</h3>
                    <h3 v-else> Description: <input type="text" v-model="Edits.Description" /></h3>
                </div>
                <div v-if="showMore">
                    <h3> AHJ Level Code: {{ this.AHJInfo ? this.AHJInfo.AHJLevelCode.Value : 'Loading' }} </h3>
                </div>
                <div class="break"/>
                <div v-if="showMore">
                    <h3 v-if="!isEditing">Document Submission Method Notes: {{ this.AHJInfo ? this.AHJInfo.DocumentSubmissionMethodNotes.Value : 'Loading' }}</h3>
                    <h3 v-else> Document Submission Method Notes: <input type="text" v-model="Edits.DocumentSubmissionMethodNotes" /></h3>
                </div>
                <div v-if="showMore">
                    <h3 v-if="!isEditing">Permit Issue Method Notes: {{ this.AHJInfo ? this.AHJInfo.PermitIssueMethodNotes.Value : 'Loading' }}</h3>
                    <h3 v-else> Permit Issue Method Notes: <input type="text" v-model="Edits.PermitIssueMethodNotes" /></h3>
                </div>
                <div class="break"/>
                <div v-if="showMore">
                    <h3 v-if="!isEditing">URL: {{ this.AHJInfo ? this.AHJInfo.URL.Value : 'Loading' }}</h3>
                    <h3 v-else> URL: <input type="text" v-model="Edits.URL" /></h3>
                </div>
                <div v-if="showMore">
                    <h3 v-if="!isEditing">File Folder URL: {{ this.AHJInfo ? this.AHJInfo.FileFolderURL.Value : 'Loading' }}</h3>
                    <h3 v-else> File Folder URL: <input type="text" v-model="Edits.FileFolderURL" /></h3>
                </div>
                <div class="break"/>
                <div v-if="showMore">
                    <h3 v-if="!isEditing">Estimated Turnaround Days: {{ this.AHJInfo ? this.AHJInfo.EstimatedTurnaroundDays.Value : 'Loading' }}</h3>
                    <h3 v-else> Estimated Turnaround Days: <input type="text" v-model="Edits.EstimatedTurnaroundDays" /></h3>
                </div>
                <div style="position:absolute;right:1%;top:92%;" id="edit-buttons">
                    <!-- OPen window to display edits on this page -->
                    <a v-if="!isEditing" style="margin:0;padding:0;margin-right:10px;text-decoration: underline; cursor:pointer;" v-on:click="showBigDiv('edits')">Show Edits</a>
                    <!-- Allow user to edit this AHJ -->
                    <a id="editButton" v-if="!isEditing" style="margin:0;padding:0;text-decoration: underline; cursor:pointer;" v-on:click="editing()">Edit This AHJ</a>
                    <!-- Open window to display edits -->
                    <a v-else style="margin:0;padding:0;text-decoration: underline; margin-right:10px; cursor:pointer;" v-on:click="showBigDiv('confirm-edits'); createEditObjects();">Submit Edits</a>
                    <!-- Cancel user made edits without submitting -->
                    <a v-if="isEditing" style="margin:0;padding:0;text-decoration: underline; cursor:pointer;" v-on:click="isEditing = false;">Cancel</a>
                </div>
            </div>
        </div>
        <div id='body'>
            <div id='tableDiv'>
                <div class="title-card">
                    <h2 class="title">Codes</h2>
                </div>
                <!-- Table to display codes -->
                <table class="table" border=1 frame=void rules=rows>
                    <tbody>
                        <tr v-on:click="toggleShow('BCNotes')">
                            <td style="width:49%">Building Code</td>
                            <!-- Display building code and building code notes -->
                            <td v-if="!isEditing" style="width:49%">{{ this.AHJInfo ? ahjCodeFormatter(this.AHJInfo.BuildingCode.Value) : "Loading" }}</td>
                            <td v-on:click.stop="" v-else>
                                <!-- If user is editing display dropdown -->
                                <b-form-select id="BCSelector" size="sm" v-model="Edits.BuildingCode" :options="consts.CHOICE_FIELDS.AHJ.BuildingCode" style="width:155px;"></b-form-select>
                            </td>
                            <td style="min-width:10px;width:1%;"><i id="BCNotesChev" class="fa fa-chevron-down"></i></td>
                        </tr>
                        <tr>
                            <!-- Building code notes display as dropdown -->
                            <td id='BCNotesTD' colspan="3" class="hide">
                            <div v-if="!isEditing" id='BCNotes' class='notes-bar'>{{ this.AHJInfo && this.AHJInfo.BuildingCodeNotes? this.AHJInfo.BuildingCodeNotes.Value : "No Notes" }}</div>
                            <!-- If editing display text area -->
                            <textarea v-else v-model="Edits.BuildingCodeNotes" type="text" class="notes-bar"/>
                            </td>
                        </tr>
                        <tr v-on:click="toggleShow('ECNotes')">
                            <td style="width:49%">Electrical Code</td>
                            <!-- Display Electric Code and Notes -->
                            <td v-if="!isEditing" style="width:49%">{{ this.AHJInfo ? ahjCodeFormatter(this.AHJInfo.ElectricCode.Value) : "Loading" }}</td>
                             <td v-on:click.stop="" v-else>
                                 <!-- If user is editing show dropdown -->
                                <b-form-select size="sm" v-model="Edits.ElectricCode" :options="consts.CHOICE_FIELDS.AHJ.ElectricCode" style="width:155px;"></b-form-select>
                            </td>
                            <td style="min-width:10px;width:1%;"><i id="ECNotesChev" class="fa fa-chevron-down"></i></td>
                        </tr>
                        <tr>
                            <!-- Electric code notes display as dropdown -->
                            <td id='ECNotesTD' colspan="3" class="hide">
                            <div v-if="!isEditing" id='ECNotes' class='notes-bar'>{{ this.AHJInfo && this.AHJInfo.ElectricCodeNotes? this.AHJInfo.ElectricCodeNotes.Value : "No Notes" }}</div>
                            <!-- if editing display textarea -->
                            <textarea v-else v-model="Edits.ElectricalCodeNotes" type="text" class="notes-bar"/>
                            </td>
                        </tr>
                        <tr v-on:click="toggleShow('FCNotes')">
                            <td style="width:49%">Fire Code</td>
                            <!-- Fire Code and notes display -->
                            <td v-if="!isEditing" style="width:49%">{{ this.AHJInfo ? ahjCodeFormatter(this.AHJInfo.FireCode.Value) : "Loading" }}</td>
                             <td v-on:click.stop="" v-else>
                                 <!-- if Editing change to dropdown menu -->
                                <b-form-select size="sm" v-model="Edits.FireCode" :options="consts.CHOICE_FIELDS.AHJ.FireCode" style="width:155px;"></b-form-select>
                            </td>
                            <td style="min-width:10px;width:1%;"><i id="FCNotesChev" class="fa fa-chevron-down"></i></td>
                        </tr>
                        <tr>
                            <!-- Fire code notes display as dropdown -->
                            <td colspan="3" class="hide" id="FCNotesTD">
                            <div v-if="!isEditing" id='FCNotes' class='notes-bar'>{{ this.AHJInfo && this.AHJInfo.FireCodeNotes? this.AHJInfo.FireCodeNotes.Value : "No Notes" }}</div>
                            <!-- if Editing change to textarea -->
                            <textarea v-else v-model="Edits.FireCodeNotes" type="text" class="notes-bar"/>
                            </td>
                        </tr>
                        <tr v-on:click="toggleShow('RCNotes')">
                            <td style="width:49%">Residential Code</td>
                            <!-- Display residential code and notes -->
                            <td v-if="!isEditing" style="width:49%">{{ this.AHJInfo ? ahjCodeFormatter(this.AHJInfo.ResidentialCode.Value) : "Loading" }}</td>
                             <td v-on:click.stop="" v-else>
                                 <!-- if Editing, display as dropdown menu -->
                                <b-form-select size="sm" v-model="Edits.ResidentialCode" :options="consts.CHOICE_FIELDS.AHJ.ResidentialCode" style="width:155px;"></b-form-select>
                            </td>
                            <td style="min-width:10px;width:1%;"><i id="RCNotesChev" class="fa fa-chevron-down"></i></td>
                        </tr>
                        <tr>
                            <!-- Residential Code notes display as dropdown -->
                            <td colspan="3" class="hide" id="RCNotesTD">
                            <div v-if="!isEditing" id='RCNotes' class='notes-bar'>{{ this.AHJInfo && this.AHJInfo.ResidentialCodeNotes ? this.AHJInfo.ResidentialCodeNotes.Value : "No Notes" }}</div>
                            <!-- if is editing, display as textarea -->
                            <textarea v-else v-model="Edits.ResidentialCodeNotes" type="text" class="notes-bar"/>
                            </td>
                        </tr>
                        <tr v-on:click="toggleShow('WCNotes')">
                            <td style="width:49%">Wind Code</td>
                            <!-- Display wind code and notes -->
                            <td v-if="!isEditing" style="width:49%">{{ this.AHJInfo ? ahjCodeFormatter(this.AHJInfo.WindCode.Value) : "Loading" }}</td>
                             <td v-on:click.stop="" v-else>
                                 <!-- if is editing display as dropdown -->
                                <b-form-select size="sm" v-model="Edits.WindCode" :options="consts.CHOICE_FIELDS.AHJ.WindCode" style="width:155px;"></b-form-select>
                            </td>
                            <td style="min-width:10px;width:1%;"><i id="WCNotesChev" class="fa fa-chevron-down"></i></td>
                        </tr>
                        <tr>
                            <!-- Wind code notes display as dropdown -->
                            <td id='WCNotesTD' colspan="3" class="hide">
                            <div v-if="!isEditing" id='WCNotes' class='notes-bar'>{{ this.AHJInfo && this.AHJInfo.WindCodeNotes ? this.AHJInfo.WindCodeNotes.Value : "No Notes" }}</div>
                            <!-- if is editing display as textarea -->
                            <textarea v-else v-model="Edits.WindCodeNotes" type="text" class="notes-bar"/>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <!-- Contact info -->
            <div id="contactDiv">
                <div class="title-card">
                    <h2 class="title">Contact Information</h2>
                    <i v-if="isEditing" v-on:click="showBigDiv('addacontact');" class="fa fa-plus plus-button" />
                </div>
                <div id="contactInfoDiv" ref="contactInfoDiv">
                    <!-- If no contacts, display text -->
                   <h3 v-if="!(AHJInfo !== null && AHJInfo.Contacts.length > 0)" class="no-info">No contact info is available for this AHJ</h3>
                   <div v-if="(AHJInfo !== null && AHJInfo.Contacts.length > 0)">
                       <!-- Else display all contatcs -->
                        <contact-card v-for="contact in AHJInfo.Contacts" v-bind:key="`dispcont${contact.ContactID.Value}`" v-bind:data="contact"/>
                    </div>
                </div>
            </div>
            <!-- Document Submission Methods -->
            <div class="half-table">
                <div class="title-card">
                    <h2 class="title">Document Submission Methods</h2>
                    <i v-if="isEditing" v-on:click="showBigDiv('addadsub');" class="fa fa-plus plus-button" />
                </div>
                <!-- If no DSM display text -->
                <h3 v-if="!(AHJInfo !== null && AHJInfo.DocumentSubmissionMethods.length > 0)" class="no-info"> No document submission method info is available for this AHJ</h3>
                <div v-else v-for="d in AHJInfo.DocumentSubmissionMethods" v-bind:key="`dispdsm${d.UseID}`" style="background-color: white">
                    <!-- else display all DSM -->
                    <h2 class="pmdsm"> {{d.Value}} <i v-if="isEditing" v-on:click="DSMDeletion.Value.push(d.UseID)" style="float:right;" class="fa fa-minus"></i></h2>
                </div>
            </div>
            <!-- Engineering review requirements -->
            <div class="half-table">
                <div class="title-card">
                    <h2 class="title">Engineering Review Requirements</h2>
                    <!-- if is editing, allow additions -->
                    <i v-if="isEditing" v-on:click="showBigDiv('addaerr');" class="fa fa-plus plus-button" />
                </div>
                <!-- if no ERR, display text -->
                <h3 v-if="!(AHJInfo !== null && AHJInfo.EngineeringReviewRequirements.length > 0)" class="no-info">No engineering review requirement info is available for this AHJ</h3>
                   <div v-if="(AHJInfo !== null && AHJInfo.EngineeringReviewRequirements.length > 0)">
                       <!-- else display all ERR -->
                        <err-card v-for="e in AHJInfo.EngineeringReviewRequirements" v-bind:key="`diserrr${e.EngineeringReviewRequirementID.Value}`" v-bind:data="e" v-bind:editing="false"/>
                    </div>
            </div>
            <!-- Fee Structures -->
            <div class="half-table">
                <div class="title-card">
                    <h2 class="title">Fee Structures</h2>
                    <!-- if is editing allow additions -->
                    <i v-if="isEditing" v-on:click="showBigDiv('addafstruct');" class="fa fa-plus plus-button" />
                </div>
                <!-- if no fee structures display text -->
                <h3 v-if="!(AHJInfo !== null && AHJInfo.FeeStructures.length > 0)" class="no-info">No fee structure info is available for this AHJ</h3>
                   <div v-if="(AHJInfo !== null && AHJInfo.FeeStructures.length > 0)">
                       <!-- Else display all Fee Structures -->
                        <fs-card v-for="e in AHJInfo.FeeStructures" v-bind:key="`dispfs${e.FeeStructurePK.Value}`" v-bind:data="e" v-bind:editing="false"/>
                    </div>
            </div>
            <!-- Permit issue methods -->
            <div class="half-table">
                <div class="title-card">
                    <h2 class="title">Permit Issue Methods</h2>
                    <!-- if is editing, allow additions -->
                    <i v-if="isEditing" v-on:click="showBigDiv('addapermitissue');" class="fa fa-plus plus-button" />
                </div>
                <!-- if no PIM, display text -->
                <h3 v-if="!(AHJInfo !== null && AHJInfo.PermitIssueMethods.length > 0)" class="no-info"> No permit issue method info is available for this AHJ</h3>
                <div v-else v-for="d in AHJInfo.PermitIssueMethods" v-bind:key="`disPIM${d.UseID}`" style="background-color: white">
                    <!-- else display all PIM -->
                    <h2 class="pmdsm"> {{d.Value}} <i v-if="isEditing" v-on:click="PIMDeletion.Value.push(d.UseID)" style="float:right;" class="fa fa-minus"></i></h2>
                </div>
            </div>
            <!-- Inspections -->
            <div style="width:100%;" class="half-table">
                <div class="title-card">
                    <h2 class="title">AHJ Inspections</h2>
                    <!-- if is editing allow additions -->
                    <i v-if="isEditing" v-on:click="showBigDiv('addainspection');" class="fa fa-plus plus-button" />
                </div>
                <!-- if no Inspections, display text -->
                <h3 v-if="AHJInfo !== null && this.AHJInfo.AHJInspections.length == 0" class="no-info"> No inspections are available for this AHJ</h3>
                <div v-if="AHJInfo !== null && this.AHJInfo.AHJInspections.length >= 0">
                    <!-- else display all inspections -->
                    <inspection v-for="(i,index) in this.AHJInfo.AHJInspections" v-bind:key="`dispinsp${index}`" v-bind:data="i" v-bind:AHJPK="AHJInfo.AHJPK.Value" v-bind:index="index"></inspection>
                </div>
            </div>
            <div v-if="AHJInfo !== null" style="margin-top:25px;margin-bottom:25px;width:100%;">
                <!-- display all comments -->
                Comments {{this.AHJInfo !== null ? this.numComments + this.AHJInfo.Comments.length : "0"}}
                <div style="margin-top:0px;margin-bottom:25px;border-bottom:1px solid black;width:100%;height:0px;"/>
                <form  v-if="$store.getters.authToken !== ''" @submit="submitComment()" style="margin-bottom:15px;">
                    <!-- submit a comment text area -->
                    <textarea v-model="commentInput" placeholder="Type a Comment..." type="text" class="input-comment"> </textarea>
                    <b-button class="mr-2" @submit.prevent="submitComment()" type="submit">Submit</b-button>
                </form>
                <!-- if user is not logged in, disallow comment submissions -->
                <h3 style="margin-bottom:25px;" v-else> You must be logged in to leave a comment!</h3>
                <comment-card style="margin-bottom: 25px;" @count="countReplies" v-for="comment in this.AHJInfo.Comments" v-bind:key="`dispcomment${comment.CommentID.Value}`" v-bind:Comment="comment" v-bind:Reply="false">
                </comment-card>
            </div>
            <div v-else style="margin-top:25px;margin-bottom:25px;border-bottom:1px solid black;width:100%;">
                No Comments
            </div>
        </div>
    </div>
</template> 

<script>
import L from "leaflet";
import constants from '../constants.js';
import ContactCard from "../components/AHJPage/ContactCard.vue";
import CommentCard from '../components/AHJPage/CommentCard';
import EditObject from '../components/AHJPage/EditObject.vue';
import Inspection from '../components/AHJPage/Inspection.vue';
import EngineeringReviewRequirements from '../components/AHJPage/EngineeringReviewRequirements.vue';
import FeeStructure from '../components/AHJPage/FeeStructure.vue';
import axios from "axios";

export default {
    data() {
        return {
            isEditing: false,
            bigDivOpen: false,
            //string address to display
            AddressString: "",
            //address city, county, and state as string
            CityCountyState: "",
            //AHJ Info from backend
            AHJInfo: null,
            leafletMap: null,
            //for map display
            polygonLayer: null,
            striped: false,
            //comment v-model
            commentInput: "",
            numComments: 0,
            //edit changes made on AHJ, for v-models
            Edits: {
                BuildingCode: "",
                BuildingCodeNotes: "",
                ElectricCode: "",
                ElectricCodeNotes: "",
                FireCode: "",
                FireCodeNotes: "",
                ResidentialCode: "",
                ResidentialCodeNotes: "",
                WindCode: "",
                WindCodeNotes: "",
                Description: "",
                DocumentSubmissionMethodNotes: "",
                PermitIssueMethodNotes: "",
                EstimatedTurnaroundDays: "",
                FileFolderURL: "",
                URL: ""
            },
            //constants file
            consts: constants,
            //all edit objects to sent to back end
            editObjects: [],
            //contact addition to send to backend
            contactAddition: {
                SourceTable: "Contact",
                ParentTable: "AHJ",
                ParentID: null,
                AHJPK: null,
                Value: []
            },
            //inspection contact additions to backend
            inspectionContactAddition: {
                SourceTable: "Contact",
                ParentTable: "AHJInspection",
                ParentID: null,
                AHJPK: null,
                Value: []
            },
            //inspection additions to send to backend
            inspectionAddition: {
                SourceTable: "AHJInspection",
                ParentTable: "AHJ",
                ParentID: null,
                AHJPK: null,
                Value: []
            },
            //contact deletions to send to backend
            contactDeletions: {
                SourceTable: "Contact",
                AHJPK: null,
                Value: []
            },
            //inspection deletions to send to backend
            inspectionDeletions: {
                SourceTable: "AHJInspection",
                AHJPK: null,
                Value: []
            },
            //ERR deletions, for backend
            ERRDeletions: {
                SourceTable: "EngineeringReviewRequirement",
                AHJPK: null,
                Value: []
            },
            //FS Deletions for backend
            FSDeletions: {
                SourceTable: "FeeStructure",
                AHJPK: null,
                Value: []
            },
            //DSM Deletions for backend
            DSMDeletion: {
                SourceTable: "DocumentSubmissionMethod",
                AHJPK: null,
                Value: []
            },
            //PIM deletions for backend
            PIMDeletion: {
                SourceTable: "PermitIssueMethod",
                AHJPK: null,
                Value: []
            },
            //v-model for contact additions fields
            AddCont: {
                Address: {
                    AddrLine1: "",
                    AddrLine2: "",
                    AddrLine3: "",
                    City: "",
                    County: "",
                    StateProvince: "",
                    Country: "",
                    ZipPostalCode: "",
                    AddressType: "",
                    Description: "",
                },
                FirstName: "",
                LastName: "",
                WorkPhone: "",
                MiddleName: "",
                HomePhone: "",
                MobilePhone: "",
                Email: "",
                URL: "",
                Description: "",
                ContactTimezone: "",
                ContactType: "",
                PreferredContactMethod: "",
                Title: ""
            },
            //JS Doesnt deep copy nested objects, so we need this as a v-model and copy manually on edit submission
            Address: {
                    AddrLine1: "",
                    AddrLine2: "",
                    AddrLine3: "",
                    City: "",
                    County: "",
                    StateProvince: "",
                    Country: "",
                    ZipPostalCode: "",
                    AddressType: "",
                    Description: "",
            },
            //Inspection addition v-model
            AddInsp: {
                AHJPK: null,
                AHJInspectionName: "",
                AHJInspectionNotes: "",
                Description: "",
                FileFolderURL: "",
                InspectionType: "",
                TechnicianRequired: false,
                Contacts: []
            },
            technicianRequiredOptions:[
                { value: false, text: "no"},
                { value: true, text: "yes"}
            ],
            //ERR additions v-model
            AddERR: {
                EngineeringReviewType: "",
                RequirementLevel: "",
                RequirementNotes: "",
                StampType: "",
                Description: ""
            },
            //ERR addition object sent to backend
            ERRAddition: {
                AHJPK: null,
                ParentTable: "AHJ",
                ParentID: null,
                SourceTable: 'EngineeringReviewRequirement',
                Value: []
            },
            //FS addition model for backend
            FSAddition: {
                AHJPK: null,
                ParentTable: "AHJ",
                ParentID: null,
                SourceTable: 'FeeStructure',
                Value: []
            },
            //FS object for v-model
            AddFS: {
                FeeStructureName: "",
                FeeStructureType: "",
                Description: "",
                FeeStructureID: "",
            },
            //DSM string for v-model
            DSM: "",
            //DSM additions for backend
            AddDSM: {
                AHJPK: null,
                ParentTable: "AHJ",
                ParentID: null,
                SourceTable: "DocumentSubmissionMethod",
                Value: []
            },
            //PIM addition for backend
            AddPIM:{
                AHJPK: null,
                ParentTable: "AHJ",
                ParentID: null,
                SourceTable: "PermitIssueMethod",
                Value: []
            },
            Location: {
                Description: "",
                LocationDeterminationMethod: "",
                LocationType: ""
            },
            //String for PIM v-model
            PIM: "",
            //these represent indeces within arrays when someone wants to edit an addition before submitting edits
            replacingCont: -1,
            replacingInsp: -1,
            replacingInspCont: -1,
            replacingERR: -1,
            replacingFS: -1,
            AdditionOnInsp: [],
            inspEditing: -1,
            editingCont: -1,
            //list of all edits
            editList: [],
            //these represent the combined confirmed and unconfirmed entities
            allContacts: [],
            allInspections: [],
            allERR: [],
            allFS: [],
            allDSM: [],
            allPIM: [],
            //if current user is an AHJOfficial
            isManaged: false,
            contactAdditionBackup: null,
            showMore: false,
            baseFields: new Set(["URL","Description","DocumentSubmissionMethodNotes","PermitIssueMethodNotes", "EstimatedTurnaroundDays","FileFolderURL"])
        }
    },
    computed: {
        isAHJOfficial(){
            //check if user is logged in and an official of this AHJ
            return this.$store.getters.loggedIn && this.$store.state.currentUserInfo.MaintainedAHJs.includes(parseInt(this.$route.params.AHJID));
        },
        AHJID(){
            //get AHJID from URL
            return this.$route.params.AHJID;
        }
    },
    components: {
        //Components needed
        "comment-card": CommentCard,
        "contact-card": ContactCard,
        "inspection": Inspection,
        "edit-object": EditObject,
        "err-card": EngineeringReviewRequirements,
        "fs-card": FeeStructure
    },
    async mounted(){
        if (this.$store.getters.loggedIn && !this.$store.getters.currentUserInfo){
            //if page reloaded, we need to retrieve user information, if they are logged in
            await this.$store.dispatch('getUserInfo');
        }
        //fires after mount
        this.$nextTick(() => {
            //Get info for this AHJ
            this.$store.commit("callAPISingleAHJ", this.$route.params.AHJID);
            let queryString = 'AHJPK=' + this.$route.params.AHJID;
            //Get edits on this AHJ (this may be slow so we do it asynchronously)
            this.$store.commit("getEdits",queryString);
        })
    },
    methods: {
        //set up map view for page header
        setupLeaflet() {
            //info leaflet needs about map (we want it not to move)
            let leafletMap = L.map(this.$refs.map, {            
                dragging: false,
                zoomControl: false,
                scrollWheelZoom: false
            }).setView(constants.MAP_INIT_CENTER, constants.MAP_INIT_ZOOM);
            //Map won't zoom when clicked
            leafletMap.doubleClickZoom.disable();
            //set this object's leaflet map (for the map div)
            this.leafletMap = leafletMap;
            //Add a title to this map
            L.tileLayer(constants.MAP_TILE_API_URL, {
                attribution: constants.MAP_TILE_API_ATTR
            }).addTo(this.leafletMap);
        },
        //Displays this AHJ's polygon on map
        setPolygon() {
            //find this AHJs polygons
            let polygons = this.$store.state.apiData.results['ahjlist']
                .map(ahj => ahj.Polygon );
            polygons = polygons.filter(function(p){ if(!p){return false} return true; })
                //create the polygon layer
            if(polygons && polygons.length > 0){
                this.polygonLayer = L.geoJSON(polygons, {
                    style: constants.MAP_PLYGN_SYTLE
                });
                //add it to leaflet map
                this.polygonLayer.addTo(this.leafletMap);
                //display only the polygon on map
                this.leafletMap.fitBounds(this.polygonLayer.getBounds());
            }
        },
        //for manual dropdown chevrons
        toggleShow(elementId){
            //Find element's table row and toggle show/hide
            document.getElementById(elementId + "TD").classList.toggle('show');
            document.getElementById(elementId + "TD").classList.toggle('hide');
            //find associated chevron and toggle up/down
            document.getElementById(elementId + "Chev").classList.toggle('fa-chevron-down');
            document.getElementById(elementId + "Chev").classList.toggle('fa-chevron-up');
        },
        //Format ahj codes
        ahjCodeFormatter(value) {
            if(value) {
                if (value === "NoSolarRegulations") {
                  return "No Solar Regulations";
                } else if (value === "SpecialWindZone") {
                  return "Special Wind Zone";
                }
                //Add spaces between identifier and code data i.e. 2020IBC -> 2020 IBC
                return value.substring(0, 4) + " " + value.substring(4);
            }
            return value;
        },
        //format address properly
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
        //Show the window to allow additions of entities, i.e. Contact Additions
        showBigDiv(elementId){
            //scroll to top
            window.scrollTo(0,0);
            //If window was already open
            if(this.bigDivOpen){
                //enable scrolling
                document.documentElement.style.overflow = 'scroll';
                this.bigDivOpen = false;
                //Cycle through child elements and find inspections
                for(let i = 0; i < this.$children.length;i++){
                    //if insepction is adding contacts, find them and add them to the insepction object on this AHJ
                    if(this.$children[i].AddingConts == true){
                        this.$children[i].addToContacts([...this.AdditionOnInsp]);
                    }
                }
                //if user was editing an unsubmitted edit, clear it
                this.inspEditing = -1;
                this.AdditionOnInsp = [];
                //clear all deletions
                this.contactDeletions.Value = [];
                this.inspectionDeletions.Value = [];
                this.ERRDeletions.Value = [];
                this.FSDeletions.Value = [];
                this.PIMDeletion.Value = [];
                this.DSMDeletion.Value = [];
                for(let i = 0; i < this.$children[i].length;i++){
                    if(this.$children[i].Type === "AHJInspection"){
                        this.$children[i].Deleted.Value = [];
                    }
                }
            }
            //Window was not already open
            else{
                //disallow scrolling
                document.documentElement.style.overflow = 'hidden';
                this.bigDivOpen = true;
                for(let i = 0; i < this.$children.length;i++){
                    //find inspections and get all contact additions
                    if(this.$children[i].AddingConts == true){
                        this.AdditionOnInsp = this.$children[i].getPendingContacts();
                    }
                }
            }
            //find the window we want to display and toggle show/hide
            document.getElementById(elementId).classList.toggle('hide');
            document.getElementById(elementId).classList.toggle('show');
            //clear all edits of unsubmitted edits
            this.replacingCont = -1;
            this.replacingInsp = -1;
            this.replacingInspCont = -1;
        },
        //if user wants to edit
        editing(){
            //if user isn't logged in, alert and return
            if (!this.$store.getters.loggedIn) {
                alert("You must be logged in to Edit!");
                return;
            }
            //else set isEditing to opposite value
            if(this.isEditing == true){
                this.isEditing = false;
            }
            else{
                this.isEditing = true;
            }
        },
        //user submits a comment
        submitComment(){
            //disallow empty comments
            if(this.commentInput == ""){
                alert("Comment Cannot Be Empty");
                return;
            }
            //get submission url
            let url = constants.API_ENDPOINT + 'ahj/comment/submit/';
            //send comment info to backend, with th AHJID
            let data = { CommentText: this.commentInput, AHJPK: this.AHJInfo.AHJPK.Value };
            axios
                .post(url, data, {
                    headers: {
                        Authorization: this.$store.getters.authToken
                    }
                })
                .then(response => {
                    //on response, add comment to top of list of comments
                    this.AHJInfo.Comments = [response.data, ...this.AHJInfo.Comments];
                    response.data = "";
                    this.commentInput = "";
                })
        },
        //count comment replies (recursive method)
        countReplies(num){
            this.numComments += num;
        },
        //create edit object to send to backend
        createEditObjects(){
            //this.editObjects = [];
            let keys = Object.keys(this.Edits);
            for(var i = 0; i < keys.length; i++){
                //check if edit is not empty or has been changed
                if(this.Edits[keys[i]] !== "" && this.Edits[keys[i]] !== this.AHJInfo[keys[i]].Value){
                    //check if edit value isnt none
                    if(!(this.Edits[keys[i]] === "" && this.AHJInfo[keys[i]].Value === "None")){
                        let obj = {};
                        //create edit object and append to all edits
                        obj['AHJPK'] = this.AHJInfo.AHJPK.Value;
                        obj['InspectionID'] = null;
                        obj['SourceTable'] = 'AHJ';
                        obj['SourceRow'] = this.AHJInfo.AHJPK.Value;
                        obj['SourceColumn'] = keys[i];
                        obj['OldValue'] = this.AHJInfo[keys[i]].Value;
                        obj['NewValue'] = this.Edits[keys[i]];
                        this.editObjects.push(obj);
                    }
                }
            }
            //loop through all children objects
            for(let i = 0; i < this.$children.length; i++){
                //if child is editable
                if(this.$children[i].Edits){
                    let e = this.$children[i].Edits;
                    let keys = Object.keys(e);
                    for(let j = 0; j < keys.length; j++){
                        //if edit is not empty or edit has changed current data
                        if(this.$children[i].data[keys[j]] && this.$children[i].data[keys[j]].Value !== this.$children[i].Edits[keys[j]] && this.$children[i].Edits[keys[j]] !== ""){
                            //create object and append to all edit objects
                            let obj = {};
                            obj['AHJPK'] = this.AHJInfo.AHJPK.Value;
                            obj['InspectionID'] = null;
                            obj['SourceTable'] = this.$children[i].Type;
                            obj['SourceRow'] = this.$children[i].ID;
                            obj['SourceColumn'] = keys[j];
                            obj['OldValue'] = this.$children[i].data[keys[j]].Value;
                            obj['NewValue'] = this.$children[i].Edits[keys[j]];
                            this.editObjects.push(obj);
                        }
                    }
                    //if child has editable childre, get those edits
                    this.editObjects = this.editObjects.concat(this.$children[i].getEditObjects());
                }
            }
            //get children deletions
            for(i = 0; i < this.$children.length; i++){
                if(this.$children[i].Type === "AHJInspection"){
                    this.$children[i].getDeletions();
                }
                //if child has been deleted, add to proper deletion object
                if(this.$children[i].isDeleted){
                    if(this.$children[i].Type === "Contact"){
                        this.contactDeletions.Value.push(this.$children[i].data.ContactID.Value);
                    }
                    if(this.$children[i].Type === "AHJInspection"){
                        this.inspectionDeletions.Value.push(this.$children[i].data.InspectionID.Value);
                    }
                    if(this.$children[i].Type === "EngineeringReviewRequirements"){
                        this.ERRDeletions.Value.push(this.$children[i].data.EngineeringReviewRequirementID.Value);
                    }
                    if(this.$children[i].Type === "FeeStructure"){
                        this.FSDeletions.Value.push(this.$children[i].data.FeeStructurePK.Value);
                    }
                }
            }
        },
        //clear all edits on this AHJ
        clearEdits(){
            let k = Object.keys(this.Edits);
            for(let i = 0; i < k.length; i++){
                this.Edits[k[i]] = this.AHJInfo[k[i]].Value;
            }
        },
        deleteEdit(index){
            let e = this.editObjects[index];
            if(e.SourceTable === "AHJInspection"){
                for(let i = 0; i < this.$children.length; i++){
                    if(this.$children[i].ID == e.SourceRow && this.$children[i].Type === "AHJInspection"){
                        this.$children[i].Edits[e.SourceColumn] = e.OldValue;
                    }
                }
            }
            //contact
            else if(e.SourceTable === "Contact" && e.Inspection === null){
                for(let i = 0; i < this.$children.length; i++){
                    if(this.$children[i].ID == e.SourceRow && this.$children[i].Type === "Contact"){
                        this.$children[i].Edits[e.SourceColumn] = e.OldValue;
                    }
                }
            }
            //contact on inspection
            else if(e.SourceTable === "Contact" && e.InspectionID !== null){
                for(let i = 0; i < this.$children.length; i++){
                    if(this.$children[i].ID == e.InspectionID && this.$children[i].Type === "AHJInspection" && this.$children[i].eID < 0){
                        for(let j = 0; j < this.$children[i].$children.length;j++){
                            if(this.$children[i].$children[j].ID == e.SourceRow){
                                this.$children[i].$children[j].Edits[e.SourceColumn] = e.OldValue;
                                break;
                            }
                        }
                    }
                }
            }
            else{
                //else this must be on this AHJ, so reset value
                this.Edits[this.editObjects[index]['SourceColumn']] = this.editObjects[index]['OldValue'];
            }
            //remove edit object from list
            this.editObjects.splice(index,1);
        },
        //remove contact addition from list
        deleteContactAddition(index){
            this.contactAddition.Value.splice(index,1);
        },
        //delete contact addition from an inspection
        deleteInspectionContactAddition(index,ind){
            let i = this.$children[index];
            i.AddCont.Value.splice(ind,1)
        },
        //delete an inspection addition on this AHJ
        deleteInspectionAddition(index){
            this.inspectionAddition.Value.splice(index,1);
        },
        //delete an contact deletion edit
        deleteContactDeletion(index){
            //find contact child element and set its deleted flag to false
            for(let i = 0; i < this.$children.length; i++){
                if(this.$children[i].data && this.$children[i].data.ContactID && this.$children[i].data.ContactID.Value == this.contactDeletions.Value[index]){
                    this.$children[i].isDeleted = false;
                    break;
                }
            }
            this.contactDeletions.Value.splice(index,1);
        },
        //delete an inspection deletion object 
        deleteInspectionDeletion(index){
            //find inspection child object and set its deleted flag to false
            for(let i = 0; i < this.$children.length; i++){
                if(this.$children[i].data && this.$children[i].data.AHJInspectionID && 
                this.$children[i].data.InspectionID.Value == this.inspectionDeletions.Value[index]){
                    this.$children[i].isDeleted = false;
                    break;
                }
            }
            this.inspectionDeletions.Value.splice(index,1);
        },
        //delete an ERR deletion edit
        deleteERRDeletion(index){
            //find proper child object and set its deleted flag to false
            for(let i = 0; i < this.$children.length; i++){
                if(this.$children[i].data && this.$children[i].data.EngineeringReviewRequirementID && 
                this.$children[i].data.EngineeringReviewRequirementID.Value == this.ERRDeletions.Value[index]){
                    this.$children[i].isDeleted = false;
                    break;
                }
            }
            this.ERRDeletions.Value.splice(index,1);
        },
        //delete FS deletion edit
        deleteFSDeletion(index){
            //find proper child object and ser its deleted flag to false
            for(let i = 0; i < this.$children.length; i++){
                if(this.$children[i].data && this.$children[i].data.FeeStructurePK && 
                this.$children[i].data.FeeStructurePK.Value == this.FSDeletions.Value[index]){
                    this.$children[i].isDeleted = false;
                    break;
                }
            }
            this.FSDeletions.Value.splice(index,1);
        },
        //when  user wants to submit all edits
        submitEdits(){
            //get update url
            let url = constants.API_ENDPOINT + 'edit/update/';
            //send edit objects to backend
            axios
                .post(url,this.editObjects, {
                    headers: {
                        Authorization: this.$store.getters.authToken
                    }
                })
                //clear edit objects
            this.editObjects = [];
            //clear all edits on child objects 
            for(let i = 0; i < this.$children.length; i++){
                if(this.$children[i].Edit){
                    this.$children[i].clearEdits();
                }
            }
            //addition endpoint
            url = constants.API_ENDPOINT + 'edit/add/';
            for(var i = 0; i < this.contactAddition.Value.length;i++){
                let keys = Object.keys(this.contactAddition.Value[i].Address);
                for(var j = 0; j < keys.length; j++){
                    this.contactAddition.Value[i].Address[keys[j]] = this.contactAddition.Value[i].Address[keys[j]];
                }
            }
            this.contactAddition.Value = [...this.contactAddition.Value];
            //submit all addition objects to backend (this order is random)
            axios
                .post(url,JSON.stringify(this.contactAddition), {
                    headers: {
                        Authorization: this.$store.getters.authToken,
                        'Content-type': 'application/json'
                    }
                })
            axios
                .post(url,JSON.stringify(this.inspectionAddition), {
                    headers: {
                        Authorization: this.$store.getters.authToken,
                        'Content-type': 'application/json'
                    }
                })

            axios
                .post(url,this.AddPIM, {
                    headers: {
                        Authorization: this.$store.getters.authToken
                    }
                })
            axios
                .post(url,this.AddDSM, {
                    headers: {
                        Authorization: this.$store.getters.authToken
                    }
                })
            axios
                .post(url,this.ERRAddition, {
                    headers: {
                        Authorization: this.$store.getters.authToken
                    }
                })
            axios
                .post(url,this.FSAddition, {
                    headers: {
                        Authorization: this.$store.getters.authToken
                    }
                })
            //addition object on all inspection children on this AHJ
            for(let i = 0; i < this.$children.length; i++){
                if(this.$children[i].AddCont){
                    axios
                    .post(url, this.$children[i].AddCont,{
                        headers: {
                            Authorization: this.$store.getters.authToken
                        }})
                    .then(() => {});
                }
            }
            //edit deletion url
            url = constants.API_ENDPOINT + 'edit/delete/';
            //send all edit deletion objects to backend
            axios
                .post(url,this.contactDeletions, {
                    headers: {
                        Authorization: this.$store.getters.authToken
                    }
                })
            axios
                .post(url,this.inspectionDeletions, {
                    headers: {
                        Authorization: this.$store.getters.authToken
                    }
                })
            axios
                .post(url,this.ERRDeletions, {
                    headers: {
                        Authorization: this.$store.getters.authToken
                    }
                })
            axios
                .post(url,this.FSDeletions, {
                    headers: {
                        Authorization: this.$store.getters.authToken
                    }
                })
            axios
                .post(url,this.PIMDeletion, {
                    headers: {
                        Authorization: this.$store.getters.authToken
                    }
                })
            axios
                .post(url,this.DSMDeletion, {
                    headers: {
                        Authorization: this.$store.getters.authToken
                    }
                })
            //clear all edit values
            this.editObjects = [];
            this.contactAddition.Value = [];
            this.contactDeletions.Value = [];
            this.inspectionDeletions.Value = [];
            this.inspectionAddition.Value = [];
            this.ERRDeletions.Value=[];
            this.DSMDeletion.Value=[];
            this.PIMDeletion.Value=[];
            this.FSDeletions.Value=[];
            this.AddDSM.Value=[];
            this.AddPIM.Value=[];
            this.ERRAddition.Value=[];
            this.FSAddition.Value=[];
            this.AdditionOnInsp = [];
            this.reset();
            this.isEditing = false;
            let k = Object.keys(this.AddCont);
            //reset contact addition address value
            for(let i = 0; i < k.length; i++){
                if(k[i] != "Address"){
                    this.AddCont[k[i]] = "";
                }
                else{
                    let a_k = Object.keys(this.AddCont[k[i]]);
                    for(let j = 0; j < a_k.length; j++){
                        this.AddCont[k[i]][a_k[j]] = "";
                    }
                }
            }
            //close window
            this.showBigDiv('confirm-edits');
            //delete all edit objects on children
            for(let i = 0; i < this.$children.length; i++){
                if(this.$children[i].Type === "AHJInspection" && this.$children[i].eID < 1){
                    this.$children[i].delete();
                }
                if(this.$children[i].editable){
                    this.$children[i].clearEdits();
                }
            }
            for(let i = 0; i < this.$children.length; i++){
                if(this.$children[i].Edits){
                    this.$children[i].clearEdits();
                }
            }
            //clear edit object on this AHJ
            this.clearEdits();
        },
        //reset all edit objects on this AHJ
        reset(){
            this.Edits.BuildingCode = this.AHJInfo.BuildingCode.Value;
            this.Edits.FireCode = this.AHJInfo.FireCode.Value;
            this.Edits.ElectricCode = this.AHJInfo.ElectricCode.Value;
            this.Edits.WindCode = this.AHJInfo.WindCode.Value;
            this.Edits.ResidentialCode = this.AHJInfo.ResidentialCode.Value;
            this.Edits.BuildingCodeNotes = this.AHJInfo.BuildingCodeNotes.Value === 'None' ? '' : this.AHJInfo.BuildingCodeNotes.Value;
            this.Edits.ResidentialCodeNotes = this.AHJInfo.ResidentialCodeNotes.Value === 'None' ? '' : this.AHJInfo.ResidentialCodeNotes.Value;
            this.Edits.FireCodeNotes = this.AHJInfo.FireCodeNotes.Value === 'None' ? '' : this.AHJInfo.FireCodeNotes.Value;
            this.Edits.WindCodeNotes = this.AHJInfo.WindCodeNotes.Value === 'None' ? '' : this.AHJInfo.WindCodeNotes.Value;
            this.Edits.ElectricCodeNotes = this.AHJInfo.ElectricCodeNotes.Value === 'None' ? '' : this.AHJInfo.ElectricCodeNotes.Value;
            this.Edits.Description = this.AHJInfo.Description.Value === 'None' ? '' : this.AHJInfo.Description.Value;
            this.Edits.EstimatedTurnaroundDays = this.AHJInfo.EstimatedTurnaroundDays.Value === 'None' ? '' : this.AHJInfo.EstimatedTurnaroundDays.Value;
            this.Edits.DocumentSubmissionMethodNotes = this.AHJInfo.DocumentSubmissionMethodNotes.Value === 'None' ? '' : this.AHJInfo.DocumentSubmissionMethodNotes.Value;
            this.Edits.PermitIssueMethodNotes = this.AHJInfo.PermitIssueMethodNotes.Value === 'None' ? '' : this.AHJInfo.PermitIssueMethodNotes.Value;
            this.Edits.URL = this.AHJInfo.URL.Value === 'None' ? '' : this.AHJInfo.URL.Value;
            this.Edits.FileFolderURL = this.AHJInfo.FileFolderURL.Value === 'None' ? '' : this.AHJInfo.FileFolderURL.Value;
        },
        //user creates a contact addition edit
        addContact(){
            //deep copy address into contact object
            this.$set(this.AddCont, 'Address',{ ...this.Address });
            this.AddCont.Address.Location = {...this.Location};
            //if we are not replacing a contact
            if(this.replacingCont < 0){
                //if we are not adding to an inspection, push to contact addition object
                if(this.inspEditing < 0){
                    this.contactAddition.Value.push({
                        ...this.AddCont
                    });
                }
                //else push to inspection contact object
                else{
                    this.AdditionOnInsp.push({
                        ...this.AddCont
                    });
                }
            }
            //else
            else{
                if(this.inspEditing < 0){
                    //if not on inspection, replace contact at value with edited contact
                    this.contactAddition.Value.splice(this.replacingCont, 1, {
                        ...this.AddCont
                    });
                }
                else{
                    //else do it on inspection  contact
                    this.AdditionOnInsp.splice(this.replacingCont, 1, {
                        ...this.AddCont
                    });
                }
                //reset
                this.replacingCont = -1;
            }
            //clear fields
            let k = Object.keys(this.AddCont);
            for(let i = 0; i < k.length; i++){
                if(k[i] === "Address"){
                    continue;
                }
                    this.AddCont[k[i]] = "";
            }
            k = Object.keys(this.Address);
            for(let i = 0; i < k.length; i++){
                this.Address[k[i]] = "";
            }
            // this.showBigDiv('addacontact');
        },
        //adding an inspection
        addInspection(){
            //if not replacing an already made edit
            if(this.replacingInsp < 0){
                //push to addition object
                this.inspectionAddition.Value.push({
                    ...this.AddInsp
                });
            }
            //if replacing an already made edit
            else{
                //add addition at correct index
                this.inspectionAddition.Value.splice(this.replacingInsp,1,{...this.AddInsp});
                this.replacingInsp = -1;
            }
            //clear fields
            let k = Object.keys(this.AddInsp);
            for(let i = 0; i < k.length; i++){
                if(k[i] == "Contacts"){
                    this.AddInsp[k[i]] = [];
                }
                else if(k[i] == 'AHJPK'){
                    continue;
                }
                else{
                    this.AddInsp[k[i]] = "";
                }
            }
            // this.showBigDiv('addainspection');
        },
        //add contact to inspection
        addInspectionCont(){
            //deep copy address
            this.AddCont.Address = { ...this.Address };
            this.AddCont.Address.Location = {...this.Location};
            //if not replacing an already made edit, push to addition object
            if(this.replacingInspCont < 0){
                this.AddInsp.Contacts.push({ ...this.AddCont});
            }
            //if replacing an edit, replace at proper index
            else{
                this.AddInsp.Contacts.splice(this.replacingCont,1,{ ...this.AddCont});
                this.replacingInspCont = -1;
            }
            //clear fields
            let k = Object.keys(this.AddCont);
            for(let i = 0; i < k.length; i++){
                if(k[i] === "Address"){
                    continue;
                }
                        this.AddCont[k[i]] = "";
            }
            k = Object.keys(this.Address);
            for(let i = 0; i < k.length; i++){
                    this.Address[k[i]] = "";
            }
        },
        //if user wants to replace an already made edit, set fields to that edit's information
        returnInspectionCont(index){
            this.replacingInspCont = index;
            this.AddCont = { ...this.AddInsp.Contacts[index]};
            this.Address = { ...this.AddInsp.Contacts[index].Address }
        },
        //delete an inspection contact edit
        deleteInspectionCont(index){
            //remove it from list
            this.AddInsp.Contacts.splice(index,1);
            let k = Object.keys(this.AddCont);
            //clear fields
            if(this.replacingCont == index){
                for(let i = 0; i < k.length; i++){
                if(k[i] === "Address"){
                    continue;
                }
                        this.AddCont[k[i]] = "";
            }
            }
            k = Object.keys(this.Address);
            for(let i = 0; i < k.length; i++){
                this.Address[k[i]] = "";
            }
            this.replacingInspCont = -1;
        },
        //delete a contact deletion edit
        deleteCont(index){
            //if not on inspection, remove from contacts object
            if(this.inspEditing < 0){
                this.contactAddition.Value.splice(index,1);
            }
            //else remove from inspection contacts object
            else{
                this.AdditionOnInsp.splice(index,1);
            }
            //clear fields
            let k = Object.keys(this.AddCont);
            if(this.replacingCont == index){
                for(let i = 0; i < k.length; i++){
                if(k[i] === "Address"){
                    continue;
                }
                    this.AddCont[k[i]] = "";
            }
            }
            k = Object.keys(this.Address);
            for(let i = 0; i < k.length; i++){
                this.Address[k[i]] = "";
            }
            this.replacingInspCont = -1;
            this.replacingCont = -1;
        },
        //if user wants edit an already made edit
        returnCont(index){
            //if not on inspection find contact and update fields with its info
            if(this.inspEditing < 0){
                this.replacingCont = index;
                this.AddCont = { ...this.contactAddition.Value[index]};
                this.Address = { ...this.contactAddition.Value[index].Address };
            }
            //else find inspection contact and update fields with its info
            else{
                this.replacingCont = index;
                this.AddCont = { ...this.AdditionOnInsp[index]};
                this.Address = { ...this.AdditionOnInsp[index].Address };
            }
        },
        //user wants to edit an inspectiona addition object
        returnInspectionAddition(index){
            //find the object and update fields with its info
            this.replacingInsp = index;
            this.AddInsp = { ...this.inspectionAddition.Value[index]};
        },
        //user want to add DSM
        addDSM(){
            //add to addition object
            this.AddDSM.Value = [...this.AddDSM.Value, { Value: this.DSM }];
            this.DSM = "";
        },
        //user want to remove a DSM addition object
        deleteDSMAddition(index){
            //remove from deletion object
            this.AddDSM.Value.splice(index,1);
        },
        //user wants to remove a PIM addition oblect
        deletePIMAddition(index){
            //remove from addition object
            this.AddPIM.Value.splice(index,1);
        },
        //add a PIM to the correct addition object
        addPIM(){
            this.AddPIM.Value = [...this.AddPIM.Value, { Value: this.PIM } ];
            this.PIM = "";
        },
        //remove ERR addition from the addition object
        deleteERRAddition(index){
            this.ERRAddition.Value.splice(index,1)
        },
        //remove FS addition from the addition object
        deleteFSAddition(index){
            this.FSAddition.Value.splice(index,1);
        },
        //if user wants to update an already made ERR addition
        returnERRAddition(index){
            //find in Addition object and update fields with its info
            this.replacingERR = index;
            this.AddERR = { ...this.ERRAddition.Value[index] };
        },
        //if user wants to update an already made FS addition
        returnFSAddition(index){
            //find in Addition object and update fields with its info
            this.replacingFS = index;
            this.AddFS = { ...this.FSAddition.Value[index] };
        },
        //Add ERR to addition object
        addERR(){
            //if not replacing an ERR addition, push to addition object
            if(this.replacingERR < 0){
                this.ERRAddition.Value.push({...this.AddERR});
            }
            //else find object at correct index and replace
            else{
                this.ERRAddition.Value.splice(this.replacingERR,1,{...this.AddERR});
                this.replacingERR = -1;
            }
            let k = Object.keys(this.AddERR);
            for(let i = 0; i < k.length; i++){
                this.AddERR[k[i]] = '';
            }
        },
        //Add FS to addition object
        addFS(){
            //if not replacing an FS addition, push to addition object
            if(this.replacingFS <  0){
                this.FSAddition.Value.push({...this.AddFS});
            }
            //else find object at correct index and replace
            else{
                this.FSAddition.Value.splice(this.replacingFS,1,{...this.AddFS});
                this.replacingFS = -1;
            }
            let k = Object.keys(this.AddFS);
            for(let i = 0; i < k.length; i++){
                this.AddFS[k[i]] = '';
            }
        },
        //delete a contact on an inspection
        deleteContonInsp(index,i){
            //find contact on the correct inspection and reset its deleted flag
            let insp = this.$children[index]
            for(let j = 0; j < insp.$children.length; j++){
                if(insp.$children[j].Type === "Contact" && insp.$children[j].data.ContactID.Value == insp.Deleted.Value[i]){
                    insp.$children[j].isDeleted = false;
                }
            }
            insp.Deleted.Value.splice(i,1);
        },
        //see if this AHJ is managed by the current user
        assertIsManaged(){
            if (!this.$store.getters.loggedIn) {
              this.isManaged = false;
              return;
            }
            if(this.$store.state.currentUserInfo.is_superuser){
                this.isManaged = true;
                return;
            }
            let MA =  this.$store.state.currentUserInfo.MaintainedAHJs;
            for(let i = 0; i < MA.length;i++){
                if(MA[i]==this.AHJInfo.AHJPK.Value){
                    this.isManaged = true;
                    break;
                }
            }
        },
        //if an AHJ official accepts or rejects an edit
        handleOfficial(event){
            let o = {};
            //set status of edit (accepted or rejected)
            o['EditID'] = event.eID;
            if(event.Type === 'Accept'){
                o['Status'] = 'A';
            }
            else{
                o['Status'] = 'R';
            }
            //send to backend
            let url = constants.API_ENDPOINT + 'edit/review/';
            axios
                .post(url,o, {
                    headers: {
                        Authorization: this.$store.getters.authToken
                    }
                })
        },
        //change status of DSM or PIM edit objects
        changeStatus(ref,type){
            //if accepted, set color to green
            if(type==="A"){
                this.$refs[ref][0].style.backgroundColor = '#B7FFB3';
            }
            //if rejected, set color to red
            if(type==="R"){
                this.$refs[ref][0].style.backgroundColor = '#FFBEBE';
            }
        },
        clearAddrAndLocation(){
            let keys = Object.keys(this.Address);
            for(let i = 0; i < keys.length; i++){
                this.Address[keys[i]] = '';
            }
            keys = Object.keys(this.Location);
            for(let i = 0; i < keys.length; i++){
                this.Location[keys[i]] = '';
            }
        },
        editAddress(){
            this.editObjects = [];
            var contAddr = null;
            if(this.editingCont > -1){
                for(var i = 0; i  < this.$children.length; i++){
                    if(this.$children[i].Type === 'Contact' && this.$children[i].data.ContactID.Value == this.editingCont){
                        contAddr = {...this.$children[i].data.Address};
                    }
                }
            }
            else{
                contAddr = {...this.AHJInfo.Address};
            }
            var keys = Object.keys(this.Address);
            for(i = 0; i < keys.length; i++){
                if(keys[i] !== 'Location'){
                    if(contAddr[keys[i]].Value !== this.Address[keys[i]] && this.Address[keys[i]]){
                        var obj = {};
                        obj['AHJPK'] = this.AHJInfo.AHJPK.Value;
                        obj['SourceTable'] = 'Address'
                        obj['SourceColumn'] = keys[i]
                        obj['SourceRow'] = contAddr.AddressID.Value
                        obj['OldValue'] = contAddr[keys[i]].Value
                        obj['NewValue'] = this.Address[keys[i]] 
                        this.editObjects.push(obj);
                    }
                }
            }
            keys = Object.keys(this.Location);
            for(var j = 0; j < keys.length; j++){
                        if(contAddr.Location[keys[j]].Value !== this.Location[keys[j]] && this.Location[keys[j]]){
                            var obj2 = {};
                            obj2['AHJPK'] = this.AHJInfo.AHJPK.Value;
                            obj2['SourceTable'] = 'Location'
                            obj2['SourceColumn'] = keys[j]
                            obj2['SourceRow'] = contAddr.Location.LocationID.Value
                            obj2['OldValue'] = contAddr.Location[keys[j]].Value
                            obj2['NewValue'] = this.Location[keys[j]] 
                            this.editObjects.push(obj2);
                        }
                    }
            this.clearAddrAndLocation();
            this.showBigDiv('addressLoc');
            this.editingCont = -1;
            return;
        },
        changeCont(index){
            this.editingCont = index;
        },
        setAddrAndLocation(){
            var contAddr = null;
            if(this.editingCont > -1){
                for(var i = 0; i  < this.$children.length; i++){
                    if(this.$children[i].Type === 'Contact' && this.$children[i].data.ContactID.Value == this.editingCont){
                        contAddr = {...this.$children[i].data.Address};
                    }
                }
            }
            else{
                contAddr = {...this.AHJInfo.Address};
            }
            let keys = Object.keys(this.Address);
            for(let i = 0; i < keys.length; i++){
                this.Address[keys[i]] = contAddr[keys[i]].Value;
            }
            keys = Object.keys(this.Location);
            for(let i = 0; i < keys.length; i++){
                this.Location[keys[i]] = contAddr.Location[keys[i]].Value;
            }
        },
        toggleMoreInfo(){
            document.getElementById("moreInfoChev").classList.toggle('fa-chevron-down');
            document.getElementById("moreInfoChev").classList.toggle('fa-chevron-up');
            this.showMore = !this.showMore;
            if(this.showMore){
                this.$refs.titleInfo.style.height = "350px"
            }
            else{
                this.$refs.titleInfo.style.height = "275px";
            }
        }
    },
    watch: {
        //when API data comes in
        '$store.state.apiData': function(){
            // If apiData is null or undefined, the passed in AHJID was invalid. Go to AHJ not found.
            if (this.$store.state.apiData.count === 0){
                let unknownType = 'AHJ';
                this.$router.push({ name: 'not-found', params: { unknownType }});
            }
            this.AHJInfo = this.$store.state.apiData.results['ahjlist'][0];
            var keys = Object.keys(this.AHJInfo);
            //replace '' with 'None
            for(var i = 0; i < keys.length; i++){
                if(this.AHJInfo[keys[i]] && this.AHJInfo[keys[i]].Value == ''){
                    this.AHJInfo[keys[i]].Value = 'None';
                }
            }
            //Set AHJPK values in edit object to the correct value
            this.reset();
            this.inspectionAddition.AHJPK = this.AHJInfo.AHJPK.Value;
            this.inspectionAddition.ParentID = this.AHJInfo.AHJPK.Value;
            this.inspectionContactAddition.AHJPK = this.AHJInfo.AHJPK.Value;
            this.contactAddition.ParentID = this.AHJInfo.AHJPK.Value;
            this.contactAddition.AHJPK = this.AHJInfo.AHJPK.Value;
            this.contactDeletions.AHJPK = this.AHJInfo.AHJPK.Value;
            this.inspectionDeletions.AHJPK = this.AHJInfo.AHJPK.Value;
            this.ERRDeletions.AHJPK = this.AHJInfo.AHJPK.Value;
            this.FSDeletions.AHJPK = this.AHJInfo.AHJPK.Value;
            this.DSMDeletion.AHJPK = this.AHJInfo.AHJPK.Value;
            this.PIMDeletion.AHJPK = this.AHJInfo.AHJPK.Value;
            this.AddInsp.AHJPK = this.AHJInfo.AHJPK.Value;
            this.AddPIM.AHJPK = this.AHJInfo.AHJPK.Value;
            this.AddPIM.ParentID = this.AHJInfo.AHJPK.Value;
            this.AddDSM.AHJPK = this.AHJInfo.AHJPK.Value;
            this.AddDSM.ParentID = this.AHJInfo.AHJPK.Value;
            this.ERRAddition.AHJPK = this.AHJInfo.AHJPK.Value;
            this.ERRAddition.ParentID = this.AHJInfo.AHJPK.Value;
            this.FSAddition.AHJPK = this.AHJInfo.AHJPK.Value;
            this.FSAddition.ParentID = this.AHJInfo.AHJPK.Value;
            this.formatAddress(this.AHJInfo.Address);
            this.allContacts = [...this.AHJInfo.Contacts,...this.AHJInfo.UnconfirmedContacts];
            this.allInspections = [...this.AHJInfo.AHJInspections, ...this.AHJInfo.UnconfirmedInspections];
            this.allERR = [...this.AHJInfo.EngineeringReviewRequirements,...this.AHJInfo.UnconfirmedEngineeringReviewRequirements];
            this.allFS = [...this.AHJInfo.FeeStructures,...this.AHJInfo.UnconfirmedFeeStructures];
            this.allDSM = [...this.AHJInfo.DocumentSubmissionMethods,...this.AHJInfo.UnconfirmedDocumentSubmissionMethods];
            this.allPIM = [...this.AHJInfo.PermitIssueMethods,...this.AHJInfo.UnconfirmedPermitIssueMethods];
            //check if current user manages this AHJ
            this.assertIsManaged();
            this.setupLeaflet();
            this.setPolygon();
        },
        //when edit list comes in, collect it
        '$store.state.editList': function(){
            var list = this.$store.state.editList;
            this.editList = [...list];
        }
    }
}
</script>

<style scoped>
#titleCard{
    position: relative;
    height: 275px;
    width: 75%;
    left: 12.5%;
    background-color: ghostwhite;
    top: 5px;
    border-radius: 5px;
    box-shadow: 2px 2px gray;
    overflow: hidden;
    margin-bottom: 50px;
}
#mapDiv{
    position: relative;
    height: 172.5px;
    width: 100%;
    border-bottom: 1px solid black;
}
#body{
    position: relative;
    width: 75%;
    left: 12.5%;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    flex-wrap: wrap;
}
#tableDiv{
    position: relative;
    border-radius: 5px;
    box-shadow: 2px 2px gray;
    width: 60%;
    height: 100%;
    margin: 0;
    overflow: hidden;
    align-self: stretch;
}
#contactDiv{
    position: relative;
    border-radius: 5px;
    box-shadow: 2px 2px gray;
    width: 35%;
    background-color: ghostwhite;
    border: 1px black;
    vertical-align: middle;
}
#contactInfoDiv{
    vertical-align: middle;
    text-align: center;
    min-height: 246px;
    width: 100%;
    overflow: hidden;
}
h1, h2, h3,td,.notes-bar, a{
  font-family: "Roboto Condensed";
  text-align: center;
  color: #4b4e52;
  margin-bottom: 0px;
}
h3, a{
  font-size: 15px;
}
#text{
    display: flex;
    justify-content: space-between;
    align-content: baseline;
    margin: 3px;
    margin-left: 5px;
    margin-right: 5px;
    border-color: black;
    border-width: 1px;
    flex-wrap: wrap;
}
table{
    margin: 0;
    border: none;
}
tr:hover{
    background-color: ghostwhite;
}
tr{
    background-color: ghostwhite;
    border-top: 1px solid black;
}
.show{
    display: table-cell;
}
.hide{
    display: none;
}
.notes-bar{
    width:100%; 
    text-align:center;
    padding: 10px;
    background-color: white;
    color: #4b4e52;
}
.half-table{
    position: relative;
    width: 47.5%;
    border-radius: 5px;
    background-color: ghostwhite;
    box-shadow: 2px 2px gray;
    margin-top: 50px;
    min-height: 270px;
}
.title-card{
    position: relative;
    border-bottom: 1px solid black;
    width: 100%;
    text-align: center;
    margin: 0;
    padding: 0;
    top: 0px;
    background-color: ghostwhite;
}
.title{
    margin: 0;
    padding: 0;
}
.no-info{
    padding-top:110px;
}
.break {
  flex-basis: 100%;
  height: 0;
}
.big-div{
    position: absolute;
    z-index: 2000;
    width: 70%;
    left: 15%;
    top: 100px;
    background-color: bisque;
    height: 75%;
    overflow-y: scroll;
}
.edits{
    position: absolute;
    z-index: 2000;
    width: 100%;
    height: 100%;
    background-color: rgb(0,0,0,0.25);
    top: 0px;
}
.edit-title{
    position: relative;
    border-bottom: 1px solid black;
    width: 98%;
    text-align: left;
    left: 1%;
    padding-top: 15px;
    font-family: "Roboto Condensed";
}
.edit-body{
    position: relative;
    min-height: 100px;
    text-align: center;
    font-family: "Roboto Condensed";
    border: 1px solid gray;
    border-top: 0px;
    width: 98%;
    left: 1%;
}
.no-border{
    border: none;
    margin-bottom: 0px;
}
.input-comment{
    width: 100%;
    border: 0px;
    border-bottom: 1px solid gray;
    margin-bottom: 5px;
}
.plus-button{
    position: absolute;
    top: 10px;
    right: 5px;
}
.edit-buttons{
  position: sticky;
  bottom: 0;
  float: right;
}
.add-cont{
    display: flex;
    justify-content: space-around;
    flex-wrap: wrap;
}
.add-breakup{
    display: flex;
    flex-direction: column;
}
.pmdsm{
    width: 100%;
    border-bottom: 1px solid black;
    text-align: center;
    font-size: 25px;;
}
.tall{
    height: 350px;
}
</style>