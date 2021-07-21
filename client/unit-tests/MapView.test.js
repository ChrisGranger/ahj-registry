/**
 * @jest-environment jsdom
 */

import { mount } from '@vue/test-utils';
import MapView from '../src/components/SearchPage/MapView';
import { createLocalVue } from '@vue/test-utils';
import { BootstrapVue, BootstrapVueIcons } from "bootstrap-vue";
import store from '../src/store.js';
import * as objects from './test_objs'; 
import AwesomeMarkers from "drmonty-leaflet-awesome-markers";

const localVue = createLocalVue();
localVue.use(BootstrapVue);
localVue.use(BootstrapVueIcons);
localVue.use(AwesomeMarkers);
const div = document.createElement('div');
document.body.appendChild(div)
const m = mount(MapView, { localVue, store, mocks: { $route: { query: "" }}, attachTo: div });

describe('Mount tests', () => {
    it('Component mounts', () => {
        expect(m.vm.previousPolygonAPIPage).toEqual("");
    });
});

describe('Method tests', () => {
    it('Get AHJ Official Address', () => {
        expect(m.vm.getAHJOfficeAddress(objects.AHJ)).toEqual("353 S 1100 E<br>Unit 12<br>Salt Lake City, Salt Lake County, UT 84102");
    });
    it('Update map markers', () => {
        store.state.apiData.results = { Location: { Latitude: { Value: null}, Longitude: {Value: null } } };
        m.vm.updateMapMarkers([{...objects.AHJ}]);
    });
});
