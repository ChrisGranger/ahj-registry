/**
 * @jest-environment jsdom
 */

import { mount } from '@vue/test-utils';
import AHJSearchPageFilter from '../src/components/SearchPage/AHJSearchPageFilter';
import { createLocalVue } from '@vue/test-utils';
import { BootstrapVue, BootstrapVueIcons } from "bootstrap-vue";
import store from '../src/store.js';
import * as objects from './test_objs';

const localVue = createLocalVue();
localVue.use(BootstrapVue);
localVue.use(BootstrapVueIcons);
var s;


beforeAll(async () => {
    s = await mount(AHJSearchPageFilter, { localVue, store, mocks: { $route: { query: "" }} });
});

describe('Mount tests', () => {
    it('Search page mounts', () => {
        expect(s.vm.filterToggled).toBe(true);
    });
    it('Mounts with query parameter', async () => {
        let s2 = await mount(AHJSearchPageFilter, { localVue, store, mocks: { $route: { query: { FireCode: "2021IFC,2018IFC" }} } });
        expect(s2.vm.parameters.FireCode).toEqual(["2021IFC","2018IFC"]);
    });
});

describe('Search filter tests', () => {
    it("Toggle search filter", () => {
        s.vm.SearchFilterToggled();
        expect(s.vm.filterToggled).toBe(false);
    });
    it("Clear filters", () => {
        var currFilter = {...s.vm.parameters };
        s.vm.parameters.BuildingCode = ['2021IBC'];
        s.vm.clearFilters();
        expect(s.vm.parameters).toEqual(currFilter);
    });
    let get_host = function() { return window.location.href; }
    it.each([
        [{AHJName: 'name'}, `${get_host()}?AHJName=name`],
        [{BuildingCode: ['2021IBC', '2018IBC']}, `${get_host()}?BuildingCode=2021IBC,2018IBC`],
        [{AHJName: 'name', AHJCode: 'code'}, `${get_host()}?AHJName=name&AHJCode=code`],
        [{AHJName: 'name', BuildingCode: ['2021IBC', '2018IBC']}, `${get_host()}?AHJName=name&BuildingCode=2021IBC,2018IBC`]
    ])('Parameterized URL', (parameters, expected) => {
        expect.assertions(1);
        Object.keys(parameters).forEach(k => s.vm.parameters[k] = parameters[k]);
        let url = s.vm.getParameterizedURL();
        expect(url).toBe(expected);
        // reset filters for next tests (clearFilters is tested above)
        s.vm.clearFilters();
    });
    it('Parameterized URL GeoJSON', () => {
        expect.assertions(1);
        store.state.searchedGeoJSON = objects.geoJSONLocation;
        s.vm.parameters.AHJName = 'Madera';
        let url = s.vm.getParameterizedURL();
        let expected = `${get_host()}?AHJName=Madera&GeoJSON=%7B%22type%22%3A%22FeatureCollection%22%2C%22features%22%3A%5B%7B%22type%22%3A%22Feature%22%2C%22properties%22%3A%7B%7D%2C%22geometry%22%3A%7B%22type%22%3A%22Point%22%2C%22coordinates%22%3A%5B-119.088827%2C36.315125%5D%7D%7D%5D%7D`;
        expect(url).toBe(expected);
        // reset filters for next tests (clearFilters is tested above)
        s.vm.clearFilters();
        store.state.searchedGeoJSON = null;
    });
    it.each([
        [{AHJName: 'name'}, {AHJName: 'name'}],
        [{BuildingCode: '2021IBC,2018IBC'}, {BuildingCode: ['2021IBC', '2018IBC']}],
        [{AHJName: 'name', AHJCode: 'code'}, {AHJName: 'name', AHJCode: 'code'}],
        [{AHJName: 'name', BuildingCode: '2021IBC,2018IBC'}, {AHJName: 'name', BuildingCode: ['2021IBC', '2018IBC']}]
    ])('Read Parameterized URL Query', (vueQueryObject, expected_values) => {
        s.vm.setQueryFromObject(vueQueryObject);
        Object.keys(expected_values).forEach(k => expect(s.vm.parameters[k]).toEqual(expected_values[k]));
        s.vm.clearFilters();
    });
    it('Read Parameterized URL Query GeoJSON', () => {
        expect.assertions(2);
        let vueQueryObject = {AHJName: 'Madera', GeoJSON: '%7B%22type%22%3A%22FeatureCollection%22%2C%22features%22%3A%5B%7B%22type%22%3A%22Feature%22%2C%22properties%22%3A%7B%7D%2C%22geometry%22%3A%7B%22type%22%3A%22Point%22%2C%22coordinates%22%3A%5B-119.088827%2C36.315125%5D%7D%7D%5D%7D'};
        s.vm.setQueryFromObject(vueQueryObject);
        expect(s.vm.parameters.AHJName).toBe(vueQueryObject.AHJName);
        expect(store.state.searchedGeoJSON).toEqual(objects.geoJSONLocation);
        // reset filters for next tests (clearFilters is tested above)
        s.vm.clearFilters();
        store.state.searchedGeoJSON = null;
    });
    let createElem = tag => document.createElement(tag);
    let addToBody = elem => document.getElementsByTagName('body')[0].appendChild(elem);
    it('Set Classes On Element', () => {
        let elem = createElem('div');
        let toAdd = ['d', 'e', 'f'];
        let toRemove = ['a', 'b', 'c'];
        toRemove.forEach(c => elem.classList.add(c));
        expect.assertions(toAdd.length + toRemove.length);
        s.vm.setClassesOnElem(elem, toAdd, toRemove);
        toAdd.forEach(c => expect(elem.classList.contains(c)).toBe(true));
        toRemove.forEach(c => expect(elem.classList.contains(c)).toBe(false));
        elem.remove();
    });
    it('Search Filter Show More Search Options', () => {
        let elems = ['drop', 'showbutton', 'hidebutton'].map(id => {
            let elem = createElem('div');
            elem.id = id;
            return elem;
        });
        elems.forEach(addToBody);
        let classes = ['show', 'dropdown-hide', 'dropdown-hide'];
        classes.forEach((c, i) => elems[i].classList.add(c));
        s.vm.show();
        expect.assertions(elems.length);
        classes.forEach((c, i) => expect(elems[i].classList.contains(c)).toBe(false));
        elems.forEach(e => e.remove());
    });
    it.each([
        [[0]],
        [[0, 0]],
        [[0, 1, 2]],
        [[0, 1, 2, 2]],
        [[0, 1, 2, 1, 0]],
        [[0, 2, 1, 1, 2, 0]],
    ])('Search Filter Toggle Dropdowns', (clicking_order) => {
        let createIds = count => name => [...Array(count).keys()].map(n => `${name}${n}`);
        let numIdsToCreate = 3;
        let nIds = createIds(numIdsToCreate);
        let dropdownIds = nIds('dropdown');
        let iconIds = nIds('icon');
        let createDropdownWithId = id => {
            let elem = addToBody(createElem('div'));
            elem.id = id;
            return elem;
        }
        let createIconWithId = id => {
            let icon = addToBody(createElem('div')).appendChild(createElem('i'))
            icon.id = id;
            return icon;
        }
        let moreThanOneClick = clicking_order.length > 1;
        let allDropdownsClosed = moreThanOneClick && clicking_order[clicking_order.length - 1] === clicking_order[clicking_order.length - 2];
        let lastOpen = clicking_order[clicking_order.length - 1];
        let dropdowns = dropdownIds.map(id => createDropdownWithId(id));
        let icons = iconIds.map(id => createIconWithId(id));
        icons.forEach(i => i.classList.add('fa-plus'));
        clicking_order.forEach(i => s.vm.toggleDropdown(dropdownIds[i], iconIds[i]));
        if (allDropdownsClosed) {
            expect.assertions(4);
            expect(document.getElementsByClassName('active').length).toBe(0);
            expect(document.getElementsByClassName('show').length).toBe(0);
            expect(document.getElementsByClassName('fa-minus').length).toBe(0);
            expect(document.getElementsByClassName('fa-plus').length).toBe(numIdsToCreate);
        } else {
            let activeDropdowns = [...document.getElementsByClassName('active')];
            let showDropdowns = [...document.getElementsByClassName('show')];
            let activeIcons = [...document.getElementsByClassName('fa-minus')];
            let allElems = activeDropdowns.concat(showDropdowns).concat(activeIcons);
            expect.assertions(4 + allElems.length);
            expect(activeDropdowns.length).toBe(1);
            expect(showDropdowns.length).toBe(1);
            expect(activeIcons.length).toBe(1);
            allElems.forEach(elem => expect(parseInt(elem.id.slice(-1))).toBe(lastOpen));
            expect(document.getElementsByClassName('fa-plus').length).toBe(numIdsToCreate - 1);
        }
        dropdowns.forEach(d => d.remove());
        icons.forEach(i => i.remove());
    });
});
