"""
This is a script of utility functions for recreating an AHJ Registry database.
The following are the file locations and structure that these functions expect the
data for upload to be in, and the general order that these functions should be called.

Expected File Tree
    ::

        ~/AHJRegistryData/:
            |-- 2020CensusPolygons/:
                |-- States/:
                    |-- tl_2020_us_state/:
                        |-- <files from Census Bureau; should have .shp file>
                |-- Counties/:
                    |-- tl_2020_us_county/:
                        |-- <files from Census Bureau; should have .shp file>
                |-- CountySubdivisions/:
                    |-- tl_2020_01_cousub/:
                        |-- <files from Census Bureau; should have .shp file>
                    ... (58 folders total)
                    |-- tl_2020_78_cousub/:
                        |-- <files from Census Bureau; should have .shp file>
                |-- Cities/:
                   |-- tl_2020_01_place/:
                       |-- <files from Census Bureau; should have .shp file>
                   ... (58 folders total)
                   |-- tl_2020_78_place/:
                       |-- <files from Census Bureau; should have .shp file>
            |-- AHJRegistryData/:
               |-- ahjregistrydata.csv
               |-- ahjcensusnames.csv (optional)
            |-- UserData/:
               |-- prod_authtoken_token.csv
               |-- prod_core_user.csv

Order to Call Functions
    #. **upload_all_shapefile_types:**

       .. note:: Often when running this function, the shell will freeze.
                 It is recommended to run each function called by this function's definition separately instead.

       Uploads Census shapefile data by calling functions that upload each type of shapefile.
       The data is uploaded into temporary tables from which they need to be copied by translate_polygons.

    #. **translate_polygons:**

       Copies the shapefile data from the temporary
       tables into the shapefile tables used by the AHJ Registry.

    #. **add_enum_values:**

       Populates the tables that store enumerated values with their values.

    #. **create_admin_user:**

       Creates an admin account with api tokens that can be used with the admin dashboard or testing the API.
       Additional admin user accounts can be created later by running 'python3 manage.py createsuperuser'.

    #. **load_ahj_data_csv:**

       Uploads AHJ data from a CSV downloaded from a running instance of the AHJ Registry.
       Must have a user account with Email = settings.ADMIN_ACCOUNT_EMAIL to run.

    #. **address_to_contacts:**

       Ensures every Contact has an Address. If a Contact does not already have an Address,
       this creates an Address row for it. This is ideally enforced by the database.

    #. **locations_to_addresses:**

       Ensures every Address has a Location. If an Address does not already have a Location,
       this creates a Location row for it. This is ideally enforced by the database.

    #. **load_ahj_census_names_ahj_table:**

        .. note:: This assumes that the AHJName values in the AHJ table are still the original names given by NREL.

       Populates the AHJCensusName table with AHJName,
       and StateProvince using those values on the AHJ table and Address table.

    #. **load_ahj_census_names_csv:**
       Populates the AHJCensusName table with AHJName,
       and StateProvince using a CSV with columns (AHJID, AHJName, StateProvince).

    #. **pair_all:**

       .. note:: Often when running this function, the shell will freeze.
                 It is recommended to run each function called by this function's definition separately instead.

       Pairs AHJs with their shapefile polygon, if it is found.
       This function calls other functions that pair each type of polygon to an AHJ.

    #. **load_user_data_csv:**

       Uploads user data from a CSV into the User and Contact tables.
"""

import csv
import os
from django.contrib.gis.utils import LayerMapping
from .models import *
from .models_field_enums import *
from .utils import ENUM_FIELDS, get_enum_value_row

BASE_DIR = os.path.expanduser('~/AHJRegistryData/')
BASE_DIR_SHP = BASE_DIR + '2020CensusPolygons/'

# Dictionaries that map fields in shapefiles to
# fields in the temporary tables (StateTemp, etc)
# to hold the shapefile data.

state_mapping = {
    'GEOID': 'GEOID',
    'NAME': 'NAME',
    'ALAND': 'ALAND',
    'AWATER': 'AWATER',
    'INTPTLAT': 'INTPTLAT',
    'INTPTLON': 'INTPTLON',
    'mpoly': 'MULTIPOLYGON'
}


county_mapping = {
    'STATEFP': 'STATEFP',
    'GEOID': 'GEOID',
    'NAME': 'NAME',
    'NAMELSAD': 'NAMELSAD',
    'ALAND': 'ALAND',
    'AWATER': 'AWATER',
    'INTPTLAT': 'INTPTLAT',
    'INTPTLON': 'INTPTLON',
    'mpoly': 'MULTIPOLYGON'
}


cousub_mapping = {
    'STATEFP': 'STATEFP',
    'GEOID': 'GEOID',
    'NAME': 'NAME',
    'NAMELSAD': 'NAMELSAD',
    'ALAND': 'ALAND',
    'AWATER': 'AWATER',
    'INTPTLAT': 'INTPTLAT',
    'INTPTLON': 'INTPTLON',
    'mpoly': 'MULTIPOLYGON'
}


city_mapping = {
    'STATEFP': 'STATEFP',
    'GEOID': 'GEOID',
    'NAME': 'NAME',
    'NAMELSAD': 'NAMELSAD',
    'ALAND': 'ALAND',
    'AWATER': 'AWATER',
    'INTPTLAT': 'INTPTLAT',
    'INTPTLON': 'INTPTLON',
    'mpoly': 'MULTIPOLYGON'
}


def upload_all_shapefile_types():
    upload_state_shapefiles()
    upload_county_shapefiles()
    upload_city_shapefiles()
    upload_countysubdivision_shapefiles()


def upload_state_shapefiles():
    for subdir in os.walk(BASE_DIR_SHP + 'States'):
        for file in subdir[2]:
            if file.endswith('.shp'):
                state_shp = os.path.join(subdir[0], file)
                lm = LayerMapping(StateTemp, state_shp, state_mapping, transform=False)
                lm.save(strict=True, verbose=True)


def upload_county_shapefiles():
    for subdir in os.walk(BASE_DIR_SHP + 'Counties'):
        for file in subdir[2]:
            if file.endswith('.shp'):
                county_shp = os.path.join(subdir[0], file)
                lm = LayerMapping(CountyTemp, county_shp, county_mapping, transform=False)
                lm.save(strict=True, verbose=True)


def upload_city_shapefiles():
    for subdir in os.walk(BASE_DIR_SHP + 'Places'):
        for file in subdir[2]:
            if file.endswith('.shp'):
                city_shp = os.path.join(subdir[0], file)
                lm = LayerMapping(CityTemp, city_shp, city_mapping, transform=False)
                lm.save(strict=True, verbose=True)


def upload_countysubdivision_shapefiles():
    for subdir in os.walk(BASE_DIR_SHP + 'CountySubdivisions'):
        for file in subdir[2]:
            if file.endswith('.shp'):
                cousub_shp = os.path.join(subdir[0], file)
                lm = LayerMapping(CousubTemp, cousub_shp, cousub_mapping, transform=False)
                lm.save(strict=True, verbose=True)


def get_polygon_fields(obj):
    return {
        'Name': obj.NAME,
        'GEOID': obj.GEOID,
        'Polygon': obj.mpoly,
        'LandArea': obj.ALAND,
        'WaterArea': obj.AWATER,
        'InternalPLatitude': obj.INTPTLAT,
        'InternalPLongitude': obj.INTPTLON
    }


def get_state_polygon_type_fields(obj, polygon):
    return {
        'PolygonID': polygon,
        'FIPSCode': obj.GEOID
    }


def get_other_polygon_type_fields(obj, polygon):
    return {
        'PolygonID': polygon,
        'StatePolygonID': StatePolygon.objects.get(FIPSCode=obj.GEOID[:2]),
        'LSAreaCodeName': obj.NAMELSAD
    }


def translate_polygons():
    """
    Moves the shapefile data from the temporary tables (StateTemp, ...)
    to the Polygon tables (Polygon, StatePolygon, ...)
    """
    translate_states()
    translate_counties()
    translate_cities()
    translate_countysubdivisions()


def translate_states():
    states = StateTemp.objects.all()
    count = states.count()
    i = 0
    for state in states:
        polygon = Polygon.objects.create(**get_polygon_fields(state))
        StatePolygon.objects.create(**get_state_polygon_type_fields(state, polygon))
        print("pair_polygons_ahjs {1}: {0:.0%}".format(i/count, StateTemp.__name__))
        i += 1


def translate_counties():
    counties = CountyTemp.objects.all()
    count = counties.count()
    i = 0
    for county in counties:
        polygon = Polygon.objects.create(**get_polygon_fields(county))
        CountyPolygon.objects.create(**get_other_polygon_type_fields(county, polygon))
        print("pair_polygons_ahjs {1}: {0:.0%}".format(i/count, CountyTemp.__name__))
        i += 1


def translate_cities():
    cities = CityTemp.objects.all()
    count = cities.count()
    i = 0
    for city in cities:
        polygon = Polygon.objects.create(**get_polygon_fields(city))
        CityPolygon.objects.create(**get_other_polygon_type_fields(city, polygon))
        print("pair_polygons_ahjs {1}: {0:.0%}".format(i/count, CityPolygon.__name__))
        i += 1


def translate_countysubdivisions():
    cousubs = CousubTemp.objects.all()
    count = cousubs.count()
    i = 0
    for cousub in cousubs:
        polygon = Polygon.objects.create(**get_polygon_fields(cousub))
        CountySubdivisionPolygon.objects.create(**get_other_polygon_type_fields(cousub, polygon))
        print("pair_polygons_ahjs {1}: {0:.0%}".format(i/count, CountySubdivisionPolygon.__name__))
        i += 1


def add_enum_values():
    """
    Adds all enum values to their enum tables.
    """
    for field in ENUM_FIELDS:
        model = apps.get_model('ahj_app', field)
        model.objects.all().delete()
        model.objects.bulk_create(list(map(lambda choice: model(Value=choice[0]),
                                           model._meta.get_field('Value').choices)))


def is_zero_depth_field(name):
    """
    Checks if a field name has one dot in it.
    For example, the string ``'BuildingCode.Value'`` has one dot.
    """
    if name.find('.') != -1 and name.find('.') == name.rfind('.'):
        return True
    return False


def dict_filter_keys_start_with(start, row):
    """
    Given a dict, returns a new dict with key-value pairs
    where the key of each pair starts with start.
    """
    return {k[len(start)+1:]: v for k, v in row.items() if k.startswith(start)}


def build_field_val_dict(row):
    """
    Builds an Orange Button AuthorityHavingJurisdiction JSON object from a flattened object.
    """
    result = {}
    done_keys = set()
    for k, v in row.items():
        field = k[:k.find('.')]
        if k == '' or v == '' or field in done_keys:  # no value or already gathered to create a dict
            continue
        elif field == 'AHJLevelCode':
            result[field] = '0' + v if len(v) < 3 else v 
        elif is_zero_depth_field(k):  # (key, value or array of values) pair
            square_loc = field.find('[')
            if square_loc >= 0:
                array_field = field[:square_loc]
                if array_field not in result:
                    result[array_field] = []
                result[array_field].append(v)
            else:
                result[field] = v
        else:  # (key, object or array of objects) pair
            subrow = dict_filter_keys_start_with(field, row)
            done_keys.add(field)
            square_loc = field.find('[')
            if square_loc >= 0:
                array_field = field[:square_loc]
                if array_field not in result:
                    result[array_field] = []
                result[array_field].append(build_field_val_dict(subrow))
            else:
                result[field] = build_field_val_dict(subrow)
    return result


def create_address(address_dict):
    location_dict = address_dict.pop('Location', None)
    if location_dict is not None:
        address_dict['LocationID'] = create_location(location_dict)
    return Address.objects.create(**address_dict)


def create_location(location_dict):
    return Location.objects.create(**location_dict)


def create_contact(contact_dict):
    address_dict = contact_dict.pop('Address', None)
    if address_dict is not None:
        contact_dict['AddressID'] = create_address(address_dict)
    else:
        contact_dict['AddressID'] = Address.objects.create()
    return Contact.objects.create(**contact_dict)


def enum_values_to_primary_key(ahj_dict):
    """
    Replace enum values in a dict with the row of the value in its enum model.
    For example, ``'2021IBC'`` is translated to the object ``BuildingCode.objects.get(Value='2021IBC')``.
    """
    for field in ahj_dict:
        if type(ahj_dict[field]) is dict:
            ahj_dict[field] = enum_values_to_primary_key(ahj_dict[field])
        elif type(ahj_dict[field]) is list:
            for i in range(len(ahj_dict[field])):
                if type(ahj_dict[field][i]) is dict:
                    ahj_dict[field][i] = enum_values_to_primary_key(ahj_dict[field][i])
                else:  # Array of enum values
                    ahj_dict[field][i] = get_enum_value_row(field, ahj_dict[field][i])
        else:
            if field in ENUM_FIELDS:
                ahj_dict[field] = get_enum_value_row(field, ahj_dict[field])
    return ahj_dict


def create_edit_objects(ahj_obj, field_string, userID, DSC, newVal):
    """
    Currently only creates edits for string fields on an AHJ.
    This is a helper for adding DataSourceComments.
    """
    edit_dict = {}
    edit_dict['AHJPK'] = ahj_obj
    edit_dict['SourceTable'] = 'AHJ'
    edit_dict['SourceColumn'] = field_string
    edit_dict['SourceRow'] = ahj_obj.AHJPK
    edit_dict['OldValue'] = ''
    edit_dict['NewValue'] = newVal
    edit_dict['DateRequested'] = datetime.date.today() - datetime.timedelta(days=1)
    edit_dict['DateEffective'] = datetime.date.today() - datetime.timedelta(days=1)
    edit_dict['ReviewStatus'] = 'A'
    edit_dict['ChangedBy'] = userID
    edit_dict['DataSourceComment'] = DSC
    edit_dict['EditType'] = 'U'
    return Edit.objects.create(**edit_dict)


def create_admin_user():
    admin_username = settings.ADMIN_ACCOUNT_USERNAME
    admin_email = settings.ADMIN_ACCOUNT_EMAIL
    admin_password = settings.ADMIN_ACCOUNT_PASSWORD
    admin = User.objects.create_user(
        Username=admin_username,
        Email=admin_email,
        password=admin_password,
        Photo="No photo"
    )
    admin.is_active = True
    admin.is_staff = True
    admin.is_superuser = True
    admin.Photo = ""
    admin.save()
    webpage_api_token = WebpageToken.objects.create(user=admin)
    api_token = APIToken.objects.create(user=admin)
    print(f'WEBPAGE API TOKEN: {webpage_api_token}')
    print(f'API TOKEN: {api_token}')


def load_ahj_data_csv():
    user = User.objects.get(Email=settings.ADMIN_ACCOUNT_EMAIL)
    with open(BASE_DIR + 'AHJRegistryData/ahjregistrydata.csv') as file:
        reader = csv.DictReader(file, delimiter=',', quotechar='"')
        i = 1
        for row in reader:
            ahj_dict = build_field_val_dict(row)
            enum_values_to_primary_key(ahj_dict)

            address_dict = ahj_dict.pop('Address', None)
            if address_dict is not None:
                ahj_dict['AddressID'] = create_address(address_dict)
            else:
                ahj_dict['AddressID'] = Address.objects.create()

            dsc = ahj_dict.pop('DataSourceComments', '')
            dsms = ahj_dict.pop('DocumentSubmissionMethods', [])
            pims = ahj_dict.pop('PermitIssueMethods', [])
            errs = ahj_dict.pop('EngineeringReviewRequirements', [])
            contacts_dict = ahj_dict.pop('Contacts', [])

            ahj = AHJ.objects.create(**ahj_dict)

            for contact_dict in contacts_dict:
                contact_dict['ParentTable'] = 'AHJ'
                contact_dict['ParentID'] = ahj.AHJPK
                contact_dict['ContactStatus'] = True
                create_contact(contact_dict)

            for dsm in dsms:
                AHJDocumentSubmissionMethodUse.objects.create(AHJPK=ahj, DocumentSubmissionMethodID=dsm, MethodStatus=1)

            for pim in pims:
                AHJPermitIssueMethodUse.objects.create(AHJPK=ahj, PermitIssueMethodID=pim, MethodStatus=1)

            for err in errs:
                err['AHJPK'] = ahj
                err['EngineeringReviewRequirementStatus'] = 1
                EngineeringReviewRequirement.objects.create(**err)

            if dsc != '':
                if ahj.BuildingCode is not None:
                    bcVal = BuildingCode.objects.get(BuildingCodeID=ahj.BuildingCode.BuildingCodeID).Value
                    create_edit_objects(ahj, 'BuildingCode', user, dsc, bcVal)

                if ahj.FireCode is not None:
                    fcVal = FireCode.objects.get(FireCodeID=ahj.FireCode.FireCodeID).Value
                    create_edit_objects(ahj, 'FireCode', user, dsc, fcVal)

                if ahj.ResidentialCode is not None:
                    rcVal = ResidentialCode.objects.get(ResidentialCodeID=ahj.ResidentialCode.ResidentialCodeID).Value
                    create_edit_objects(ahj, 'ResidentialCode', user, dsc, rcVal)

                if ahj.ElectricCode is not None:
                    ecVal = ElectricCode.objects.get(ElectricCodeID=ahj.ElectricCode.ElectricCodeID).Value
                    create_edit_objects(ahj, 'ElectricCode', user, dsc, ecVal)

                if ahj.WindCode is not None:
                    wcVal = WindCode.objects.get(WindCodeID=ahj.WindCode.WindCodeID).Value
                    create_edit_objects(ahj, 'WindCode', user, dsc, wcVal)

            print('AHJ {0}: {1}'.format(ahj.AHJID, i))
            i += 1


def get_empty_loc():
    loc = {}
    loc['Altitude'] = None
    loc['Elevation'] = None
    loc['Latitude'] = None
    loc['Longitude'] = None
    loc['Description'] = ''
    loc['LocationDeterminationMethod'] = None
    loc['LocationType'] = None
    return Location.objects.create(**loc)

def get_empty_addr():
    addr = {}
    addr['AddrLine1'] = ''
    addr['AddrLine2'] = ''
    addr['AddrLine3'] = ''
    addr['City'] = ''
    addr['County'] = ''
    addr['Country'] = ''
    addr['StateProvince'] = ''
    addr['ZipPostalCode'] = ''
    addr['Description'] = ''
    addr['AddressType'] = None
    addr['LocationID'] = get_empty_loc()
    return Address.objects.create(**addr)

def locations_to_addresses():
    addrs = Address.objects.filter(LocationID=None)
    for a in addrs:
        l = get_empty_loc()
        l.save()
        print(l)
        a.LocationID = l
        a.save()
        print(a)

def address_to_contacts():
    conts = Contact.objects.filter(AddressID=None)
    for c in conts:
        a = get_empty_addr()
        a.save()
        print(a)
        c.AddressID = a
        c.save()
        print(c)
    return
    
# Dict to translate state FIPS codes to state abbreviations
def load_ahj_census_names_csv():
    """
    Save AHJ census names from a CSV with columns:

    ======= =============== ===============
     AHJID   AHJCensusName   StateProvince
    ======= =============== ===============
    """
    with open(BASE_DIR + 'AHJRegistryData/ahjcensusnames.csv') as file:
        reader = csv.DictReader(file, delimiter=',', quotechar='"')
        i = 1
        for row in reader:
            ahj = AHJ.objects.get(AHJID=row['AHJID'])
            AHJCensusName.objects.create(AHJPK=ahj,
                                         AHJCensusName=row['AHJCensusName'],
                                         StateProvince=row['StateProvince'])
            print('AHJ {0}: {1}'.format(ahj.AHJID, i))
            i += 1


def load_ahj_census_names_ahj_table():
    """
    Save AHJName values in the AHJ table and StateProvince values in the Address table to the AHJCensusNames table.
    Use if the AHJName values still match the names given in the NREL AHJ list.
    """
    i = 1
    for ahj in AHJ.objects.all():
        AHJCensusName.objects.create(AHJPK=ahj,
                                     AHJCensusName=ahj.AHJName,
                                     StateProvince=ahj.AddressID.StateProvince)
        print('AHJ {0}: {1}'.format(ahj.AHJID, i))
        i += 1


state_fips_to_abbr = {
    '01': 'AL',
    '02': 'AK',
    '60': 'AS',
    '04': 'AZ',
    '05': 'AR',
    '81': 'BI',
    '06': 'CA',
    '08': 'CO',
    '09': 'CT',
    '10': 'DE',
    '11': 'DC',
    '12': 'FL',
    '64': 'FM',
    '13': 'GA',
    '66': 'GU',
    '15': 'HI',
    '16': 'ID',
    '17': 'IL',
    '18': 'IN',
    '19': 'IA',
    '86': 'JI',
    '67': 'JA',
    '20': 'KS',
    '21': 'KY',
    '89': 'KR',
    '22': 'LA',
    '23': 'ME',
    '68': 'MH',
    '24': 'MD',
    '25': 'MA',
    '26': 'MI',
    '71': '71',  # Territory abbr collides with state abbr
    '27': 'MN',
    '28': 'MS',
    '29': 'MO',
    '30': 'MT',
    '76': '76',  # Territory abbr collides with state abbr
    '31': 'NE',
    '32': 'NV',
    '33': 'NH',
    '34': 'NJ',
    '35': 'NM',
    '36': 'NY',
    '37': 'NC',
    '38': 'ND',
    '69': 'MP',
    '39': 'OH',
    '40': 'OK',
    '41': 'OR',
    '70': 'PW',
    '95': '95',  # Territory abbr collides with state abbr
    '42': 'PA',
    '72': 'PR',
    '44': 'RI',
    '45': 'SC',
    '46': 'SD',
    '47': 'TN',
    '48': 'TX',
    '74': 'UM',
    '49': 'UT',
    '50': 'VT',
    '51': 'VA',
    '78': 'VI',
    '53': 'WA',
    '54': 'WV',
    '55': 'WI',
    '56': 'WY'
}

# dict for translating state abbreviations to state FIPS codes
abbr_to_state_fips = dict(map(reversed, state_fips_to_abbr.items()))


def pair_all():
    """
    Helpers to assign an AHJ to its polygon by AHJName and polygon name.
    """
    AHJ.objects.all().update(PolygonID=None)
    pair_polygons(CountyPolygon)
    pair_polygons(CityPolygon)
    pair_polygons(CountySubdivisionPolygon)
    pair_state_polygons()


def pair_polygons(model):
    polgyons = model.objects.all()
    ahjs = AHJ.objects.filter(PolygonID=None).order_by('AddressID__StateProvince')
    i = 0
    total = len(ahjs)
    # Pair polygons
    current_state_fips = ''
    temp_polygons = model.objects.none()
    for ahj in ahjs:
        addr = Address.objects.get(AddressID=ahj.AddressID.AddressID)
        temp_state_fips = abbr_to_state_fips[addr.StateProvince]
        if current_state_fips != temp_state_fips:
            current_state_fips = temp_state_fips
            temp_polygons = polgyons.filter(PolygonID__GEOID__startswith=current_state_fips).order_by('LSAreaCodeName')
        polygon_index = binary_search(temp_polygons, ahj.AHJName)
        if polygon_index != -1:
            polygon = temp_polygons[polygon_index]
            ahj.PolygonID = polygon.PolygonID
            ahj.save()
        i += 1
        print("pair_polygons_ahjs {1}: {0:.0%}".format(i/total, model.__name__))


def pair_state_polygons():
    # Pair states
    states = StatePolygon.objects.all()
    i = 0
    total = len(states)
    for state in states:
        ahj = AHJ.objects.get(AHJName=state.PolygonID.Name + ' state')
        ahj.PolygonID = state.PolygonID
        ahj.save()
        i += 1
        print("pair_polygons_ahjs {1}: {0:.0%}".format(i/total, StatePolygon.__name__))


# Iterative Binary Search Function
# It returns index of x in given array arr if present,
# else returns -1
def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    mid = 0
    x = x.lower()

    while low <= high:
        mid = (high + low) // 2
        # Check if x is present at mid
        if arr[mid].LSAreaCodeName.lower() < x:
            low = mid + 1

        # If x is greater, ignore left half
        elif arr[mid].LSAreaCodeName.lower() > x:
            high = mid - 1

        # If x is smaller, ignore right half
        else:
            return mid

            # If we reach here, then the element was not present
    return -1


BASE_DIR_USER = BASE_DIR + 'UserData/'
def load_user_data_csv():
    users = {}

    # Get user information
    with open(BASE_DIR_USER + 'prod_core_user.csv') as file:
        reader = csv.DictReader(file, delimiter=',', quotechar='"')
        i = 1
        for row in reader:
            user = {}
            user['Email'] = row['email_address']
            user['password'] = row['password']
            user['Username'] = f'username{i}'
            user['FirstName'] = row['first_name']
            user['LastName'] = row['last_name']
            user['SignUpDate'] = row['date_joined'][:10]
            user['is_active'] = row['is_active']

            users[row['id']] = user
            i += 1

    with open(BASE_DIR_USER + 'prod_authtoken_token.csv') as file:
        reader = csv.DictReader(file, delimiter=',', quotechar='"')
        i = 1
        for row in reader:
            users[row['user_id']]['apitoken'] = row['key']
            print(users[row['user_id']])

    # Create users and api tokens
    i = 1
    for user in users.values():
        apitoken = user.pop('apitoken')
        firstname = user.pop('FirstName')
        lastname = user.pop('LastName')
        user['ContactID'] = Contact.objects.create(FirstName=firstname, LastName=lastname)
        user = User.objects.create(**user)
        APIToken.objects.create(key=apitoken, user=user)
        print('User {0}: {1}'.format(i, user))
        i += 1
