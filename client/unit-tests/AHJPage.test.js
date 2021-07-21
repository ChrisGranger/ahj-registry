/**
 * @jest-environment jsdom
 */

import { mount } from '@vue/test-utils';
import AHJPage from '../src/views/AHJPage.vue'
import { createLocalVue } from '@vue/test-utils';
import BootstrapVue from 'bootstrap-vue';
import store from '../src/store.js';
import * as objects from './test_objs';

const localVue = createLocalVue();
var p;
beforeAll(async () => {
  localVue.use(BootstrapVue);
   p = await mount(AHJPage, {mocks: { $route : { params: { AHJID: 1338 } } },store, localVue});
   store.state.apiData = { results: { ahjlist:  [{...objects.AHJ}]}};
});

beforeEach(async () => {})

describe('Mount tests', () => {
  it('AHJPage mounts', async function() {
    //AHJPage mounts with route
    expect(p.vm.$route.params.AHJID).toBe(1338);
  });
  it('AHJInfo changes with state', async () => {
    //changing name in state changes name
    expect(p.vm.AHJInfo.AHJName.Value).toBe("New AHJ");
  })
});

describe('Unconfirmed object tests', () => {
  it('AllInspections is set properly', () => {
    expect(p.vm.allInspections.length).toBe(1);
  });
  it('AllContacts is set properly', () => {
    expect(p.vm.allContacts.length).toBe(1);
  });
  it('AllERR is set properly', () => {
    expect(p.vm.allERR.length).toBe(1);
  });
  it('AllFS is set properly', () => {
    expect(p.vm.allFS.length).toBe(1);
  });
  it('AllDSM is set properly', () => {
    expect(p.vm.allDSM.length).toBe(1);
  });
  it('AllPIM is set properly', () => {
    expect(p.vm.allPIM.length).toBe(1);
  });
});

describe('Methods Tests',() => {
  it('Building Code formatter',() => {
    expect(p.vm.ahjCodeFormatter('2021IBC')).toBe('2021 IBC');
  });
  it('Address Formatter',() => {
    let testAddress = { 
      AddressID: { Value: 2 },
      AddrLine1: { Value: "309 Field Crest PKWY" },
      AddrLine2: { Value: "" },
      AddrLine3: { Value: "Third Thing"},
      City: { Value: "" },
      County: { Value: "" },
      StateProvince: { Value: "LA" },
      Country: { Value: "" },
      ZipPostalCode: { Value: "84102" },
      Description: { Value: "Address Description" },
      AddressType: { Value:  "Mailing" },
      Location: null
    };
    p.vm.formatAddress(testAddress);
    expect(p.vm.AddressString).toBe("309 Field Crest PKWY, Third Thing, LA, 84102");
  });
  it('Is editing when button clicked',() => {
    // save the current value of authToken so it doesn't affect other tests.
    let tempAuthToken = store.state.authToken;
    // fake a logged in user.
    store.state.authToken = '(auth token)';
    let e = p.find("#editButton");
    e.trigger("click");
    // restore the previous authToken value so to not affect other tests.
    store.state.authToken = tempAuthToken;
    expect(p.vm.isEditing).toBe(true);
  });
  it('Clear Edits works', () => {
    let e = {...p.vm.Edits};
    p.vm.Edits.BuildingCode = "Something";
    p.vm.clearEdits();
    expect(p.vm.Edits).toEqual(e);
  });
  it('Get edit objects works',()=>{
    p.vm.Edits.BuildingCode = "2012IBC";
    p.vm.createEditObjects();
    expect(p.vm.editObjects.length).toBe(1);
    p.vm.clearEdits();
  });
});

describe('Edit system tests', () => {
  it('Delete edit works',() => {
    let e = {...p.vm.Edits};
    p.vm.Edits.BuildingCode = "2012IBC";
    p.vm.createEditObjects();
    p.vm.deleteEdit(0);
    expect(p.vm.Edits).toEqual(e);
  });
  it('Delete contact addition works', () => {
    p.vm.contactAddition.Value.push({...objects.Contact});
    expect(p.vm.contactAddition.Value.length).toBe(1);
    p.vm.deleteContactAddition(0);
    expect(p.vm.contactAddition.Value.length).toBe(0);
  });
  it('Delete inspection addition works',() => {
    p.vm.inspectionAddition.Value.push({...objects.Inspection});
    expect(p.vm.inspectionAddition.Value.length).toBe(1);
    p.vm.deleteInspectionAddition(0);
    expect(p.vm.inspectionAddition.Value.length).toBe(0);
  });
  it('Delete contact deletion works', () => {
    p.vm.contactDeletions.Value.push(1);
    expect(p.vm.contactDeletions.Value.length).toBe(1);
    p.vm.deleteContactDeletion(0);
    expect(p.vm.contactDeletions.Value.length).toBe(0);
  });
  it('Delete inspection deletion works', () => {
    p.vm.inspectionDeletions.Value.push(1);
    expect(p.vm.inspectionDeletions.Value.length).toBe(1);
    p.vm.deleteInspectionDeletion(0);
    expect(p.vm.inspectionDeletions.Value.length).toBe(0);
  });
  it('Delete ERR deletion works', () => {
    p.vm.ERRDeletions.Value.push(1);
    expect(p.vm.ERRDeletions.Value.length).toBe(1);
    p.vm.deleteERRDeletion(0);
    expect(p.vm.ERRDeletions.Value.length).toBe(0);
  });
  it('Delete FS deletion works', () => {
    p.vm.FSDeletions.Value.push(1);
    expect(p.vm.FSDeletions.Value.length).toBe(1);
    p.vm.deleteFSDeletion(0);
    expect(p.vm.FSDeletions.Value.length).toBe(0);
  });
  it('Add a contact works', () => {
    p.vm.AddCont = {...objects.Contact};
    p.vm.addContact();
    expect(p.vm.contactAddition.Value.length).toBe(1);
  });
  it('Add inspection works', () => {
    p.vm.AddInsp = {...objects.Inspection};
    p.vm.addInspection();
    expect(p.vm.inspectionAddition.Value.length).toBe(1)
  });
  it('Adding a contact to an inspection works', () => {
    p.vm.AddCont = {...objects.Contact};
    p.vm.addInspectionCont();
    expect(p.vm.AddInsp.Contacts.length).toBe(1);
  });
  it('Deleting DSM addition works', () => {
    p.vm.AddDSM.Value.push("Hello!");
    expect(p.vm.AddDSM.Value.length).toBe(1);
    p.vm.deleteDSMAddition(0);
    expect(p.vm.AddDSM.Value.length).toBe(0);
    p.vm.AddDSM.Value = [];
  });
  it('Deleting PIM addition works', () => {
    p.vm.AddPIM.Value.push("Hello!");
    expect(p.vm.AddPIM.Value.length).toBe(1);
    p.vm.deletePIMAddition(0);
    expect(p.vm.AddPIM.Value.length).toBe(0);
    p.vm.AddPIM.Value = [];
  });
  it('Adding a DSM works', () => {
    p.vm.DSM = "SolarApp";
    p.vm.addDSM();
    expect(p.vm.AddDSM.Value[0]).toEqual({Value: "SolarApp"})
  });
  it('Adding a PIM works', () => {
    p.vm.PIM = "SolarApp";
    p.vm.addPIM();
    expect(p.vm.AddPIM.Value[0]).toEqual({Value: "SolarApp"})
  });
  it('Deleting an ERR addition works', () => {
    p.vm.ERRAddition.Value.push({...objects.ERR});
    p.vm.deleteERRAddition(0);
    expect(p.vm.ERRAddition.Value.length).toBe(0);
  });
  it('Deleting an FS addition works', () => {
    p.vm.FSAddition.Value.push({...objects.FS});
    p.vm.deleteFSAddition(0);
    expect(p.vm.FSAddition.Value.length).toBe(0);
  });
  it('Add ERR works',() => {
    p.vm.AddERR = {...objects.ERR};
    p.vm.addERR();
    expect(p.vm.ERRAddition.Value[0]).toEqual(objects.ERR);
  });
  it('Add FS works',() => {
    p.vm.AddFS = {...objects.FS};
    p.vm.addFS();
    expect(p.vm.FSAddition.Value[0]).toEqual(objects.FS);
  });
});

