AHJ Search API
==============

AHJ Search
----------

The AHJ Registry provides a single API endpoint for searching AHJs using various search parameters.
The following subsections describe how to use each search parameter.

**Endpoint:**
^^^^^^^^^^^^^
    ::

        POST  https://ahjregistry.sunspec.org/api/v1/ahj/

Searching by Address
^^^^^^^^^^^^^^^^^^^^

Searching by Address finds the AHJs whose jurisdiction contains a given address using the :censusshapefiles:`Census TIGER/Line Legal Boundary Shapefiles <>`.
To use this search, send a ``POST`` request with the following Orange Button OpenAPI Address object:

.. code-block:: json

    {
        "Address": {
            "AddrLine1": {
                "Value": "<value>"
            },
            "AddrLine2": {
                "Value": "<value>"
            },
            "AddrLine3": {
                "Value": "<value>"
            },
            "City": {
                "Value": "<value>"
            },
            "County": {
                "Value": "<value>"
            },
            "StateProvince": {
                "Value": "<value>"
            },
            "ZipPostalCode": {
                "Value": "<value>"
            }
        }
    }

Example:

.. code-block:: json

    {
        "Address": {
            "AddrLine1": {
                "Value": "106 W 1st St"
            },
            "City": {
                "Value": "Los Angeles"
            },
            "StateProvince": {
                "Value": "CA"
            },
            "ZipPostalCode": {
                "Value": "90012"
            }
        }
    }

Note that not all Orange Button Address fields are required.
The implementation of this search parameter uses Google Geocoding API is used to convert the address into latitude-longitude coordinates.
It is recommended to provide enough include enough fields of the Orange Button Address such that Google Maps can find the correct address.

The Address search parameter can be included with all other search parameters, except the Location search parameter.
If a Location search parameter is included, the Address search parameter is ignored.

Searching by Location
^^^^^^^^^^^^^^^^^^^^^

Searching by Location finds the AHJs whose jurisdiction contains given latitude-longitude coordinates using the :censusshapefiles:`Census TIGER/Line Legal Boundary Shapefiles <>`.
To use this search parameter, send a ``POST`` request with the following Orange Button OpenAPI Location object:


.. code-block:: json

    {
        "Location": {
            "Latitude": {
                "Value": "<value>"
            },
            "Longitude": {
                "Value": "<value>"
            }
        }
    }

For example,

.. code-block:: json

    {
        "Location": {
            "Latitude": {
                "Value": -118.2437
            },
            "Longitude": {
                "Value": 34.0522
            }
        }
    }

Both the Latitude and Longitude fields are required.

The Location search parameter can be included with all other search parameters, except the Address search parameter.
If a Location search parameter is included, the Address search parameter is ignored.

Searching by Other Parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The other search parameters offered filter based on the field values on the Orange Button AuthorityHavingJurisdiction object.

The fields that can be used to filter AHJs are:
    - :obeditorview:`AHJCode`
    - :obeditorview:`AHJID`
    - :obeditorview:`AHJLevelCode`
    - :obeditorview:`AHJName`
    - :obeditorview:`BuildingCodes <BuildingCode>`
    - :obeditorview:`ElectricCodes <ElectricCode>`
    - :obeditorview:`FireCodes <FireCode>`
    - :obeditorview:`ResidentialCodes <ResidentialCode>`
    - :obeditorview:`WindCodes <WindCode>`
    - :obeditorview:`StateProvince`

Some of these search parameters accept one value (single-select), while others accept an array of values (multi-select).
To use these search parameters, send a ``POST`` request with any of the following Orange Button OpenAPI objects:

Single-value filters:
    .. code-block:: json

        {
            "<field_name>" : {
                "Value": "<value>"
            }
        }

For example, AHJs can be filtered by AHJID:
    .. code-block:: json

        {
            "AHJID" : {
                "Value": "63e32227-7a31-4a0c-a715-20d46315cc9e"
            }
        }

The single-select fields for filtering are:
    - :obeditorview:`AHJCode`
    - :obeditorview:`AHJID`
    - :obeditorview:`AHJLevelCode`
    - :obeditorview:`AHJName`
    - :obeditorview:`StateProvince`

Multi-select filters:
    .. code-block:: json

        {
            "<field_name>" : [
                {
                    "Value": "<value>"
                }
            ]
        }

For example, AHJs can be filtered by BuildingCodes:
    .. code-block:: json

        {
            "BuildingCodes" : [
                {
                    "Value": "2021IBC"
                },
                {
                    "Value": "2018IBC"
                }
            ]
        }

The multi-select fields for filtering are:
    - :obeditorview:`BuildingCodes <BuildingCode>`
    - :obeditorview:`ElectricCodes <ElectricCode>`
    - :obeditorview:`FireCodes <FireCode>`
    - :obeditorview:`ResidentialCodes <ResidentialCode>`
    - :obeditorview:`WindCodes <WindCode>`

Combining Search Parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Any combination of search parameters can be used like so, excluding combining Address and Location search parameters.

Here is an example of coming Address, AHJLevelCode, and FireCode filters in a search:
    .. code-block:: json

        {
            "Address": {
                "AddrLine1": {
                    "Value": "106 W 1st St"
                },
                "City": {
                    "Value": "Los Angeles"
                },
                "StateProvince": {
                    "Value": "CA"
                },
                "ZipPostalCode": {
                    "Value": "90012"
                }
            },
            "AHJLevelCode": [
                {
                    "Value": "061"
                }
            ],
            "FireCodes": [
                {
                    "Value": "2021IFC"
                },
                {
                    "Value": "2018IFC"
                }
            ]
        }

API Response Example
^^^^^^^^^^^^^^^^^^^^

Here is an example response from the API.

.. code-block:: json

    {
        "count": 1,
        "next": null,
        "previous": null,
        "AuthorityHavingJurisdictions": [
            {
                "AHJID": {
                    "Value": "f97ea81a-f9c4-4195-889e-ad414b736ce5"
                },
                "AHJCode": {
                    "Value": "CA-0686300"
                },
                "AHJLevelCode": {
                    "Value": "162"
                },
                "AHJName": {
                    "Value": "Woodlake city"
                },
                "Description": {
                    "Value": ""
                },
                "DocumentSubmissionMethodNotes": {
                    "Value": ""
                },
                "PermitIssueMethodNotes": {
                    "Value": ""
                },
                "EstimatedTurnaroundDays": {
                    "Value": null
                },
                "FileFolderURL": {
                    "Value": ""
                },
                "URL": {
                    "Value": "cityofwoodlake.com"
                },
                "BuildingCode": {
                    "Value": "2018IBC"
                },
                "BuildingCodeNotes": {
                    "Value": "California Building Code 2019"
                },
                "ElectricCode": {
                    "Value": "2017NEC"
                },
                "ElectricCodeNotes": {
                    "Value": "California Electrical Code 2019"
                },
                "FireCode": {
                    "Value": "2018IFC"
                },
                "FireCodeNotes": {
                    "Value": "California Fire Code 2019"
                },
                "ResidentialCode": {
                    "Value": "2018IRC"
                },
                "ResidentialCodeNotes": {
                    "Value": "California Residential Code 2019"
                },
                "WindCode": {
                    "Value": "ASCE716"
                },
                "WindCodeNotes": {
                    "Value": ""
                },
                "Address": {
                    "AddrLine1": {
                        "Value": "350 N Valencia Blvd"
                    },
                    "AddrLine2": {
                        "Value": ""
                    },
                    "AddrLine3": {
                        "Value": ""
                    },
                    "City": {
                        "Value": "Woodlake"
                    },
                    "Country": {
                        "Value": "USA"
                    },
                    "County": {
                        "Value": ""
                    },
                    "StateProvince": {
                        "Value": "CA"
                    },
                    "ZipPostalCode": {
                        "Value": "93286"
                    },
                    "Description": {
                        "Value": ""
                    },
                    "AddressType": {
                        "Value": ""
                    },
                    "Location": {
                        "Altitude": {
                            "Value": null
                        },
                        "Elevation": {
                            "Value": null
                        },
                        "Latitude": {
                            "Value": 36.418297
                        },
                        "Longitude": {
                            "Value": -119.098582
                        },
                        "Description": {
                            "Value": ""
                        },
                        "LocationDeterminationMethod": {
                            "Value": ""
                        },
                        "LocationType": {
                            "Value": ""
                        }
                    }
                },
                "Contacts": [
                    {
                        "FirstName": {
                            "Value": "Ramon"
                        },
                        "MiddleName": {
                            "Value": ""
                        },
                        "LastName": {
                            "Value": "Lara"
                        },
                        "HomePhone": {
                            "Value": ""
                        },
                        "MobilePhone": {
                            "Value": ""
                        },
                        "WorkPhone": {
                            "Value": "(559)564-8055"
                        },
                        "ContactType": {
                            "Value": ""
                        },
                        "ContactTimezone": {
                            "Value": ""
                        },
                        "Description": {
                            "Value": ""
                        },
                        "Email": {
                            "Value": "lwaters@ci.woodlake.ca.us"
                        },
                        "Title": {
                            "Value": "City Administrator"
                        },
                        "URL": {
                            "Value": ""
                        },
                        "PreferredContactMethod": {
                            "Value": ""
                        },
                        "Address": {
                            "AddrLine1": {
                                "Value": ""
                            },
                            "AddrLine2": {
                                "Value": ""
                            },
                            "AddrLine3": {
                                "Value": ""
                            },
                            "City": {
                                "Value": ""
                            },
                            "Country": {
                                "Value": ""
                            },
                            "County": {
                                "Value": ""
                            },
                            "StateProvince": {
                                "Value": ""
                            },
                            "ZipPostalCode": {
                                "Value": ""
                            },
                            "Description": {
                                "Value": ""
                            },
                            "AddressType": {
                                "Value": ""
                            },
                            "Location": null
                        }
                    }
                ],
                "AHJInspections": [
                    {
                        "InspectionType": {
                            "Value": "Final"
                        },
                        "AHJInspectionName": {
                            "Value": "Post-Installation Electrical"
                        },
                        "AHJInspectionNotes": {
                            "Value": "All installations must be inspected."
                        },
                        "Description": {
                            "Value": ""
                        },
                        "FileFolderURL": {
                            "Value": ""
                        },
                        "TechnicianRequired": {
                            "Value": true
                        },
                        "Contacts": [
                            {
                                "FirstName": {
                                    "Value": "Jim"
                                },
                                "MiddleName": {
                                    "Value": "Garner"
                                },
                                "LastName": {
                                    "Value": "(559)586-8582"
                                },
                                "HomePhone": {
                                    "Value": ""
                                },
                                "MobilePhone": {
                                    "Value": ""
                                },
                                "WorkPhone": {
                                    "Value": ""
                                },
                                "ContactType": {
                                    "Value": ""
                                },
                                "ContactTimezone": {
                                    "Value": ""
                                },
                                "Description": {
                                    "Value": ""
                                },
                                "Email": {
                                    "Value": ""
                                },
                                "Title": {
                                    "Value": ""
                                },
                                "URL": {
                                    "Value": ""
                                },
                                "PreferredContactMethod": {
                                    "Value": ""
                                },
                                "Address": {
                                    "AddrLine1": {
                                        "Value": "4700 Elmore Road"
                                    },
                                    "AddrLine2": {
                                        "Value": ""
                                    },
                                    "AddrLine3": {
                                        "Value": ""
                                    },
                                    "City": {
                                        "Value": "Anchorage"
                                    },
                                    "Country": {
                                        "Value": "USA"
                                    },
                                    "County": {
                                        "Value": "Anchorage Municipality"
                                    },
                                    "StateProvince": {
                                        "Value": "AK"
                                    },
                                    "ZipPostalCode": {
                                        "Value": "99507"
                                    },
                                    "Description": {
                                        "Value": ""
                                    },
                                    "AddressType": {
                                        "Value": "Mailing"
                                    },
                                    "Location": null
                                }
                            }
                        ]
                    }
                ],
                "DocumentSubmissionMethods": [
                    {
                        "Value": "SolarApp"
                    },
                    {
                        "Value": "Email"
                    }
                ],
                "PermitIssueMethods": [
                    {
                        "Value": "InPerson"
                    },
                    {
                        "Value": "SolarApp"
                    }
                ],
                "EngineeringReviewRequirements": [
                    {
                        "Description": {
                            "Value": ""
                        },
                        "EngineeringReviewType": {
                            "Value": "FireMarshal"
                        },
                        "RequirementLevel": {
                            "Value": "Optional"
                        },
                        "RequirementNotes": {
                            "Value": ""
                        },
                        "StampType": {
                            "Value": ""
                        }
                    }
                ],
                "FeeStructures": [
                    {
                        "FeeStructureID": {
                            "Value": "fb9da0c4-2fb9-4606-83bc-fdb3d6293776"
                        },
                        "FeeStructureName": {
                            "Value": "Application Submission Fee"
                        },
                        "FeeStructureType": {
                            "Value": "Flat"
                        },
                        "Description": {
                            "Value": "There is a $25 application fee."
                        }
                    }
                ]
            }
        ]
    }

API Response Metadata and Pagination
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the example from the previous subsection, on the same level as the AuthorityHavingJurisdictions array in the API response, are three fields:

    - **count**: The number of AHJs returned in the AuthorityHavingJurisdictions array.
    - **next**: A url to the API endpoint to retrieve the next page of results. It is ``null`` if there is no next page.
    - **prev**: A url to the API endpoint to retrieve the previous page of results. It is ``null`` if there is no previous page.
