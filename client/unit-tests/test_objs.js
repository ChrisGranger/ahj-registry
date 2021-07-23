 
export let location = {
    LocationID: { Value: 1 },
    Altitude: { Value: 4500.0 },
    Elevation: { Value: 4500.0 },
    Latitude: { Value: 40.7608 },
    Longitude: { Value: -111.8910 },
    Description: { Value: "Loc Description" },
    LocationDeterminationMethod: { Value: "AddressGeocoding" },
    LocationType: { Value: "GeneralProximity" }
}

export let address = {
    AddressID: { Value: 1 },
    AddrLine1: { Value: "353 S 1100 E" },
    AddrLine2: { Value: "Unit 12" },
    AddrLine3: { Value: ""},
    City: { Value: "Salt Lake City" },
    County: { Value: "Salt Lake County" },
    StateProvince: { Value: "UT" },
    Country: { Value: "United States" },
    ZipPostalCode: { Value: "84102" },
    Description: { Value: "Address Description" },
    AddressType: { Value:  "Mailing" },
    Location: { ...location }
}


export let ERR = { 
    EngineeringReviewRequirementID: { Value: 1 },
    Description: { Value: "ERR Description" },
    EngineeringReviewType: { Value:  "FireMarshal" },
    RequirementLevel: { Value:  "Optional" },
    RequirementNotes: { Value: "ERR Notes" },
    StampType: { Value: "Digital" },
    AHJPK: { Value: 1},
    EngineeringReviewRequirementStatus: { Value: 1 }
}

export let FS = {
    FeeStructurePK: { Value: 1 },
    FeeStructureID: { Value: "id" },
    FeeStructureName: { Value: "FS Name" },
    FeeStructureType: { Value:  "Flat" },
    Description: { Value: "FS Description" },
    FeeStructureStatus: { Value: 1 }
}

export let DSMUse = { 
    UseID: 1,
    Value: "Email"
}

export let PIMUse = {
    UseID: 1,
    Value: "SolarApp"
}

export let Contact = {
    ContactID: { Value: 1 },
    FirstName: { Value: "Chris" },
    MiddleName: { Value: "Drew" },
    LastName: { Value: "Granger" },
    HomePhone: { Value: "3378578050" },
    WorkPhone: { Value: "3373547003" },
    MobilePhone: { Value: "" },
    ContactType: { Value:  "Homeowner"},
    ContactTimezone: { Value: "Mountain" },
    Description: { Value: "Cont Description" },
    Email: { Value: "email@email.email" },
    Title: { Value: "Title" },
    URL: { Value: "url.com" },
    PreferredContactMethod: { Value: "WorkPhone" },
    Address: { ...address },
    ContactStatus: { Value: 1 },
    ParentID: 1,
    ParentTable: "AHJ"
}

export let Inspection = { 
    AHJInspectionName: { Value: "Name" }, 
    InspectionID: { Value: 1},
    InspectionType: { Value: "RoughIn" },
    AHJInspectionNotes: { Value: "Notes" },
    Description: { Value: "Description" },
    FileFolderURL: { Value: "url" },
    TechnicianRequired: { Value: 0 },
    AHJPK: { Value: 1 },
    Contacts: [{...Contact}],
    UnconfirmedContacts: []
}

export let AHJ = {
    AHJPK: { Value: 1 },
    AHJID: { Value: "ahjid" },
    AHJCode: { Value: "LA-1" },
    AHJLevelCode: { Value: 50 },
    AHJName: { Value: "New AHJ" },
    Description: { Value: "AHJ Description" },
    DocumentSubmissionMethodNotes: { Value: "No DSM Notes" },
    PermitIssueMethodNotes: { Value: "No PIM Notes" },
    EstimatedTurnaroundDays: { Value: 1 },
    FileFolderURL: { Value: "ahj-filefolder.com" },
    URL: { Value: "ahj.com" },
    BuildingCode: { Value: "2021IBC" },
    BuildingCodeNotes: { Value: "No BC Notes" },
    ElectricCode: { Value: null },
    ElectricCodeNotes: { Value: "No EC Notes" },
    FireCode: { Value: null },
    FireCodeNotes: { Value: "No FC Notes" },
    ResidentialCode: { Value: null },
    ResidentialCodeNotes: { Value: "No RC Notes" },
    WindCode: { Value: null },
    WindCodeNotes: { Value: "No EC Notes" },
    Address: { ...address },
    Contacts: [{...Contact}],
    UnconfirmedContacts: [],
    AHJInspections: [{...Inspection}],
    UnconfirmedInspections: [],
    EngineeringReviewRequirements: [{...ERR}],
    UnconfirmedEngineeringReviewRequirements: [],
    FeeStructures: [{...FS}],
    UnconfirmedFeeStructures: [],
    DocumentSubmissionMethods: [{...DSMUse}],
    UnconfirmedDocumentSubmissionMethods: [],
    PermitIssueMethods: [{...PIMUse}],
    ConfirmedPermitIssueMethods: [],
    UnconfirmedPermitIssueMethods: [],
    Comments: [],
    Polygon: {
        type: "Feature",
        geometry: {
            type: "MultiPolygon",
            coordinates: [
                [
                    [
                        [
                            -150.426471,
                            61.167514
                        ],
                        [
                            -150.426471,
                            61.167514
                        ]
                    ]
                ]
            ]
        },
        properties: {
            AHJID: "ahjid",
            LandArea: 4420591349,
            GEOID: "02020",
            InternalPLatitude: 61.1742503,
            InternalPLongitude: -149.2843294
        }
    }
}

export let Edit = {
    DateRequested: "09-12-1998",
    OldValue: "2018IBC",
    NewValue: "2021IBC",
    SourceColumn: "BuildingCode",
    SourceRow: 1,
    SourceTable: "AHJ",
    Comments: "No comments here!",
    ChangedBy: "No one",
    ReviewStatus: "A"
}

export let geoJSONLocation = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Point",
                "coordinates": [
                    -119.088827,
                    36.315125
                ]
            }
        }
    ]
}
