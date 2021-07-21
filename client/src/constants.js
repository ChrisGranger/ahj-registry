const API_ENDPOINT = "http://localhost:8000/api/v1/";
const SUPPORT_EMAIL = "support@sunspec.org";
const MEMBERSHIP_EMAIL = "membership@sunspec.org";

export default {
  API_ENDPOINT: API_ENDPOINT,
  SUPPORT_EMAIL: SUPPORT_EMAIL,
  MEMBERSHIP_EMAIL: MEMBERSHIP_EMAIL,
  AHJ_FIELDS: {
    AHJCode: "",
    AHJName: "",
    BuildingCode: "",
    BuildingCodeNotes: "",
    ElectricCode: "",
    ElectricCodeNotes: "",
    EstimatedTurnaroundDays: "",
    FireCode: "",
    FireCodeNotes: "",
    ResidentialCode: "",
    ResidentialCodeNotes: "",
    WindCode: "",
    WindCodeNotes: "",
    DocumentSubmissionMethodNotes: "",
    PermitIssueMethodMethodNotes: "",
    FileFolderURL: "",
    URL: "",
    Description: "",
    AHJLevelCode: "",
    RecordID: "",
    Address: null,
    AHJInspections: [],
    Contacts: [],
    DocumentSubmissionMethods: [],
    EngineeringReviewRequirements: [],
    FeeStructures: [],
    PermitIssueMethods: []
  },
  CONTACT_FIELDS: { // Template for Orange Button Contact object
    RecordID: "",
    FirstName: "",
    MiddleName: "",
    LastName: "",
    Title: "",
    WorkPhone: "",
    HomePhone: "",
    MobilePhone: "",
    Email: "",
    ContactTimezone: "",
    ContactType: "",
    PreferredContactMethod: "",
    URL: "",
    Description: "",
    Address: null
  },
  ADDRESS_FIELDS: { // Template for Orange Button Address object
    RecordID: "",
    AddrLine1: "",
    AddrLine2: "",
    AddrLine3: "",
    City: "",
    County: "",
    StateProvince: "",
    ZipPostalCode: "",
    Country: "",
    AddressType: "",
    Description: "",
    Location: null
  },
  LOCATION_FIELDS: { // Template for Orange Button Location object
    RecordID: "",
    Altitude: "",
    Elevation: "",
    Longitude: "",
    Latitude: "",
    LocationType: "",
    LocationDeterminationMethod: "",
    Description: ""
  },
  ENGINEERINGREVIEWREQUIREMENTS_FIELDS: { // Template for Orange Button EngineeringReviewRequirement object
    RecordID: "",
    EngineeringReviewType: "",
    RequirementLevel: "",
    RequirementNotes: "",
    StampType: "",
    Description: ""
  },
  FEESTRUCTURE_FIELDS: { // Template for Orange Button FeeStrucutre object
    RecordID: "",
    Description: "",
    FeeStructureName: "",
    FeeStructureType: ""
  },
  AHJINSPECTION_FIELDS: { // Template for Orange Button AHJInspection object
    AHJInspectionName: "",
    AHJInspectionNotes: "",
    Description: "",
    FileFolderURL: "",
    InspectionType: "",
    TechnicianRequired: "",
    Contacts: []
  },
  DOCUMENTSUBMISSIONMETHOD_FIELDS: { // Template for Orange Button DocumentSubmisisonMethod object
    RecordID: "",
    DocumentSubmissionMethod: ""
  },
  PERMITSUBMISSIONMETHOD_FIELDS: { // Template for Orange Button PermitSubmissionMethod object
    RecordID: "",
    PermitIssueMethod: ""
  },
  CHOICE_FIELDS: { // Field enums for every choice field of Orange Button objects
    AHJ: {
      AHJLevelCode: [
        { value: "", text: "AHJ Level Code" },
        { value: "040", text: "State (040)" },
        { value: "050", text: "County (050)" },
        { value: "061", text: "MCD (061)" },
        { value: "162", text: "Place (162)" }
      ],
      BuildingCode: [
        { value: "", text: "" },
        { value: "2021IBC", text: "2021 IBC" },
        { value: "2018IBC", text: "2018 IBC" },
        { value: "2015IBC", text: "2015 IBC" },
        { value: "2012IBC", text: "2012 IBC" },
        { value: "2009IBC", text: "2009 IBC" },
        { value: "NoSolarRegulations", text: "No Solar Regulations" }
      ],
      ElectricCode: [
        { value: "", text: "" },
        { value: "2020NEC", text: "2020 NEC" },
        { value: "2017NEC", text: "2017 NEC" },
        { value: "2014NEC", text: "2014 NEC" },
        { value: "2011NEC", text: "2011 NEC" },
        { value: "2008NEC", text: "2008 NEC" },
        { value: "NoSolarRegulations", text: "No Solar Regulations" }
      ],
      FireCode: [
        { value: "", text: "" },
        { value: "2021IFC", text: "2021 IFC" },
        { value: "2018IFC", text: "2018 IFC" },
        { value: "2015IFC", text: "2015 IFC" },
        { value: "2012IFC", text: "2012 IFC" },
        { value: "2009IFC", text: "2009 IFC" },
        { value: "NoSolarRegulations", text: "No Solar Regulations" }
      ],
      ResidentialCode: [
        { value: "", text: "" },
        { value: "2021IRC", text: "2021 IRC" },
        { value: "2018IRC", text: "2018 IRC" },
        { value: "2015IRC", text: "2015 IRC" },
        { value: "2012IRC", text: "2012 IRC" },
        { value: "2009IRC", text: "2009 IRC" },
        { value: "NoSolarRegulations", text: "No Solar Regulations" }
      ],
      WindCode: [
        { value: "", text: "" },
        { value: "ASCE716", text: "ASCE7-16" },
        { value: "ASCE710", text: "ASCE7-10" },
        { value: "ASCE705", text: "ASCE7-05" },
        { value: "SpecialWindZone", text: "Special Wind Zone" }
      ]
    },
    DocumentSubmissionMethod: {
      DocumentSubmissionMethod: [
        { value: "", text: "" },
        { value: "Epermitting", text: "Epermitting" },
        { value: "Email", text: "Email" },
        { value: "InPerson", text: "In Person" },
        { value: "SolarApp", text: "SolarApp" }
      ]
    },
    PermitIssueMethod: {
      PermitIssueMethod: [
        { value: "", text: "" },
        { value: "Epermitting", text: "Epermitting" },
        { value: "Email", text: "Email" },
        { value: "InPerson", text: "In Person" },
        { value: "SolarApp", text: "SolarApp" }
      ]
    },
    Contact: {
      ContactType: [
        { value: "", text: "" },
        { value: "Homeowner", text: "Homeowner" },
        { value: "OffTaker", text: "Off Taker" },
        { value: "Inspector", text: "Inspector" },
        { value: "Engineer", text: "Engineer" },
        { value: "Originator", text: "Originator" },
        { value: "Installer", text: "Installer" },
        { value: "Investor", text: "Investor" },
        { value: "PermittingOfficial", text: "Permitting Official" },
        { value: "FireMarshal", text: "Fire Marshal" },
        { value: "ProjectManager", text: "Project Manager" },
        { value: "Salesperson", text: "Salesperson" }
      ],
      PreferredContactMethod: [
        { value: "", text: "" },
        { value: "Email", text: "Email" },
        { value: "WorkPhone", text: "Work Phone" },
        { value: "CellPhone", text: "Cell Phone" },
        { value: "HomePhone", text: "Home Phone" },
        { value: "CellTextMessage", text: "Cell Text Message" }
      ]
    },
    Address: {
      AddressType: [
        { value: "", text: "" },
        { value: "Mailing", text: "Mailing" },
        { value: "Billing", text: "Billing" },
        { value: "Installation", text: "Installation" },
        { value: "Shipping", text: "Shipping" }
      ]
    },
    Location: {
      LocationDeterminationMethod: [
        { value: "", text: "" },
        { value: "GPS", text: "GPS" },
        { value: "Survey", text: "Survey" },
        { value: "AerialImage", text: "Aerial Image" },
        { value: "EngineeringReport", text: "Engineering Report" },
        { value: "AddressGeocoding", text: "Address Geocoding" },
        { value: "Unknown", text: "Unknown" }
      ],
      LocationType: [
        { value: "", text: "" },
        { value: "DeviceSpecific", text: "Device Specific" },
        { value: "SiteEntrance", text: "Site Entrance" },
        { value: "GeneralProximity", text: "General Proximity" },
        { value: "Warehouse", text: "Warehouse" }
      ]
    },
    EngineeringReviewRequirement: {
      EngineeringReviewType: [
        { value: "", text: "" },
        { value: "StructuralEngineer", text: "Structural Engineer" },
        { value: "ElectricalEngineer", text: "Electrical Engineer" },
        { value: "PVEngineer", text: "PV Engineer" },
        { value: "MasterElectrician", text: "Master Electrician" },
        { value: "FireMarshal", text: "Fire Marshal" },
        { value: "EnvironmentalEngineer", text: "Environmental Engineer" }
      ],
      RequirementLevel: [
        { value: "", text: "" },
        { value: "Required", text: "Required" },
        { value: "Optional", text: "Optional" },
        { value: "ConditionallyRequired", text: "Conditionally Required" }
      ],
      StampType: [
        { value: "", text: "" },
        { value: "Wet", text: "Wet" },
        { value: "Digital", text: "Digital" },
        { value: "Notary", text: "Notary" }
      ]
    },
    FeeStructure: {
      FeeStructureType: [
        { value: "", text: "" },
        { value: "Flat", text: "Flat" },
        { value: "SystemSize", text: "System Size" }
      ]
    },
    AHJInspection: {
      AHJInspectionType: [
        { value: "", text: "" },
        { value: "RoughIn", text: "Rough In" },
        { value: "Final", text: "Final" },
        { value: "Windstorm", text: "Windstorm" },
        { value: "Electrical", text: "Electrical" },
        { value: "Structural", text: "Structural" }
      ],
      TechnicianRequired: [
        { value: "", text: "" },
        { value: "True", text: "True" },
        { value: "False", text: "False" }
      ]
    },
    APIEditViewMode: [
      { value: "latest", text: "Latest Edits" },
      { value: "confirmed", text: "Confirmed Edits" }
    ]
  },
  MAP_INIT_CENTER: [38, -98], // Default map focus on page load
  MAP_INIT_ZOOM: 4, // Default map zoom on page load
  MAP_TILE_API_URL: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}", // Map tile API endpoint
  MAP_TILE_API_ATTR: "Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community", // Map title API endpoint attribution
  MAP_PLYGN_SYTLE: function() { // Unselected map polygon style settings
    return {
      fillOpacity: 0.07,
      opacity: 0.3,
      color: "blue",
      weight: 2
    };
  },
  MAP_PLYGN_SLCTD_SYTLE: function() { // Selected map polyogn style settings
    return {
      fillOpacity: 0.07,
      opacity: 1,
      color: "red",
      eight: 2
    };
  },
  MAP_PLYGN_CSTM_COLOR: function(rgba) { // Map polygon style with parameterized color
    return {
      fillOpacity: 0.07,
      opacity: 1,
      color: rgba,
      eight: 2
    };
  },
  // Validators for various fields
  VALID_EMAIL: (email) => /[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*[.][a-zA-Z]+/g.test(email),
  NUM_OR_SPECIAL_CHAR: (password) => /[0-9!@#$%^&*()_+\-=[\]{};':"\\,.<>/?]+/g.test(password),
  CONTAINS_LETTER: (password) => /[A-Za-z]+/g.test(password),
  VALID_PHONE: (phone) => /\(?\d{3}\)?[\s.-]?\d{3}[\s.-]\d{4}|\d{10}/g.test(phone),
  API_USAGE_BADGE_BOUNDARIES: [50, 200, 500],
  COMMUNITY_SCORE_BADGE_BOUNDARIES: [30, 150, 400],
  ACCEPTED_EDITS_BADGE_BOUNDARIES: [3, 8, 15],
  // Message and notification text
  API_THROTTLE_MSG: `Thank you for using this service. Please consider becoming a member by contacting <a href="mailto:${MEMBERSHIP_EMAIL}">${MEMBERSHIP_EMAIL}</a> to continue searching.`
};
