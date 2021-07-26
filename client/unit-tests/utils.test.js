/**
 * @jest-environment jsdom
 */

import * as utils from '../src/utils.js';


function make_csv_row(fields) {
    return fields.join(',');
}

function make_csv_header(fields) {
    return make_csv_row(fields);
}

function make_csv(rows) {
    return [...rows, ''].join('\n');
}

describe('flattenJSON tests', () => {
    it.each([
        [{'Value': 'name'}, {'Value': 'name'}],
        [{'AHJName': {'Value': 'name'}}, {'AHJName.Value': 'name'}],
        [{'Address': {'Location': {'LocationType': {'Value': 'DeviceSpecific'}}}}, {'Address.Location.LocationType.Value': 'DeviceSpecific'}],
        [{'DocumentSubmissionMethods': [{'Value': 'SolarApp'}]}, {'DocumentSubmissionMethods[0].Value': 'SolarApp'}],
        [{'Contacts': [{'FirstName': {'Value': 'name'}}]}, {'Contacts[0].FirstName.Value': 'name'}],
        [[{'AHJName': {'Value': 'name'}}], {'[0].AHJName.Value': 'name'}],
        [{'Contacts': []}, {}]
    ])("is flattened:\n Input %p", (given, expected) => {
        expect.assertions(1);
        expect(utils.flattenJSON(given, true)).toMatchObject(expected);
    });
});

describe('jsonToCSV tests', () => {
    it.each([
        [{'Value': 'name'},
            make_csv([
                make_csv_header(['Value']),
                make_csv_row(['name'])])],
        [{'AHJName': {'Value': 'name'}},
            make_csv([
                make_csv_header(['AHJName.Value']),
                make_csv_row(['name'])])],
        [[{'AHJName': {'Value': 'name'}}],
            make_csv([
                make_csv_header(['AHJName.Value']),
                make_csv_row(['name'])])],
        [{'Address': {'Location': {'LocationType': {'Value': 'DeviceSpecific'}}}},
            make_csv([
                make_csv_header(['Address.Location.LocationType.Value']),
                make_csv_row(['DeviceSpecific'])])],
        [[{'Address': {'Location': {'LocationType': {'Value': 'DeviceSpecific'}}}}, {'Address': {'Description': {'Value': 'desc'}}}],
            make_csv([
                make_csv_header(['Address.Location.LocationType.Value', 'Address.Description.Value']),
                make_csv_row(['DeviceSpecific', '']),
                make_csv_row(['', 'desc'])])],
        [{'DocumentSubmissionMethods': [{'Value': 'SolarApp'}]},
            make_csv([
                make_csv_header(['DocumentSubmissionMethods[0].Value']),
                make_csv_row(['SolarApp'])])],
        [{'Contacts': [{'FirstName': {'Value': 'name'}}]},
            make_csv([
                make_csv_header(['Contacts[0].FirstName.Value']),
                make_csv_row(['name'])])],
        [{'AHJName': {'Value': 'name, with, commas'}},
            make_csv([
                make_csv_header(['AHJName.Value']),
                make_csv_row(['"name, with, commas"'])])],
        [[{'AHJName': {'Value': 'name'}, 'Description': {'Value': 'desc'}}],
            make_csv([
                make_csv_header(['AHJName.Value', 'Description.Value']),
                make_csv_row(['name', 'desc'])])],
        [[{'AHJName': {'Value': 'name'}}, {'AHJName': {'Value': 'name'}, 'Description': {'Value': 'second'}}],
            make_csv([
                make_csv_header(['AHJName.Value', 'Description.Value']),
                make_csv_row(['name', '']),
                make_csv_row(['name', 'second'])])],
        [[{'AHJName': {'Value': 'name'}}, {'Description': {'Value': 'desc'}}],
            make_csv([
                make_csv_header(['AHJName.Value', 'Description.Value']),
                make_csv_row(['name', '']),
                make_csv_row(['', 'desc'])])],
        [{'Address': {}},
            make_csv([])],
        [{'DocumentSubmissionMethods': []},
            make_csv([])],
        [{'Contacts': []},
            make_csv([])]
    ])("is CSV:\n Input: %p", (given, expected) => {
        expect.assertions(1);
        expect(utils.jsonToCSV(given)).toBe(expected);
    });
});
