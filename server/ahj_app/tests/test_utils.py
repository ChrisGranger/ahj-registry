from django.db import connection
from django.urls import reverse
from django.http import HttpRequest
from ahj_app.models import User, Edit, Comment, StatePolygon, AHJ, Address, Polygon
from ahj_app.models_field_enums import *
from fixtures import *
from ahj_app.utils import *
import pytest
import datetime
import requests

@pytest.fixture
def location():
    return {
        'Latitude': {
            'Value': 1
        },
        'Longitude': {
            'Value': 1
        }
    }

@pytest.fixture
def geojson_point():
    return {
            'type': 'Feature',
            'properties': {},
            'geometry': {
                'type': 'Point',
                'coordinates': [-90, 30]
            } 
        }

@pytest.fixture
def geojson_polygon():
    return {
            'geometry': {
                'coordinates': [[[-90, 30], [-90, 30], [-90, 30], [-90, 30]]],
                'type': 'Polygon',
            },
            'properties': {},
            'type': 'Feature'
        }

@pytest.fixture
def feature_collection():
    return {
        'FeatureCollection': {
            'type': 'FeatureCollection',
            'features': [{
                'type': 'Feature',
                'properties': {},
                'geometry': {
                    'type': 'Polygon',
                    'coordinates': [[
                        [-111.7, 40.97],
                        [-111.6, 40.83],
                        [-111.87, 40.81],
                        [-111.7, 40.97], 
                    ]]
                }
            }]
        }
    }

@pytest.fixture
def mpoly_obj():
    p1 = geosPolygon( ((0, 0), (0, 1), (1, 1), (0, 0)) )
    p2 = geosPolygon( ((1, 1), (1, 2), (2, 2), (1, 1)) )
    mp = MultiPolygon(p1, p2)
    return mp

def create_ahj(ahjpk, ahjid, landArea, ahjLevelCode):
    p1 = geosPolygon( ((0, 0), (0, 1), (1, 1), (0, 0)) )
    p2 = geosPolygon( ((1, 1), (1, 2), (2, 2), (1, 1)) )
    mp = MultiPolygon(p1, p2)
    polygon = Polygon.objects.create(Polygon=mp, LandArea=landArea, WaterArea=1, InternalPLatitude=1, InternalPLongitude=1)
    address = Address.objects.create()
    ahj = AHJ.objects.create(AHJPK=ahjpk, AHJID= ahjid, PolygonID=polygon, AddressID=address, AHJLevelCode=ahjLevelCode)
    return ahj
    

@pytest.mark.parametrize(
   'latVal, longVal, expected_output', [
       (None, None, None),
       (1, None, None),
       (None, 1, None),
       (1, 2, 'POINT(2.0, 1.0)'),
   ]
)
def test_get_str_location(latVal, longVal, expected_output):
    location = {
        'Latitude': {
            'Value': latVal
        },
        'Longitude': {
            'Value': longVal
        }
    }
    assert get_str_location(location) == expected_output

def test_get_str_address__regular_input():
    address = {
        'AddrLine1': { 'Value': 'line1' },
        'AddrLine2': { 'Value': 'line2' },
        'AddrLine3': { 'Value': 'line3' },
        'City': { 'Value': 'City' },
        'County': { 'Value': 'County' },
        'StateProvince': { 'Value': 'State' },
        'ZipPostalCode': { 'Value': 'Zip' },
    }
    assert get_str_address(address) == 'line1 line2 line3, City County State Zip'

def test_get_str_address__empty_input():
    assert get_str_address({}) == '  ,    '

@pytest.mark.parametrize(
   'address, expected_output', [
       (
           'University of Utah', 
       { 'Latitude': { 'Value': 40.8, }, 'Longitude': { 'Value': -111.8 }}
       ),
       ( '', { 'Latitude': { 'Value': None }, 'Longitude': { 'Value': None }}
       )
   ]
)
def test_get_location_gecode_address_str(address, expected_output):
    location = get_location_gecode_address_str(address)
    if location['Latitude']['Value'] is not None and location['Longitude']['Value'] is not None:
        location['Latitude']['Value'] = round(location['Latitude']['Value'], 1) # Round so this test case is future-proof
        location['Longitude']['Value'] = round(location['Longitude']['Value'], 1) 
    assert location == expected_output

@pytest.mark.parametrize(
   'type, val, expected_output', [
       (None, None, ''),
       ('AHJName', None, ''),
       (None, 'Test', ''),
       ('AHJName', 'Test', 'AHJ.AHJName LIKE %(AHJName)s AND '),\
   ]
)
def test_get_name_query_cond(type, val, expected_output):
    assert get_name_query_cond(type,val, {}) == expected_output

@pytest.mark.parametrize(
   'type, val, expected_output', [
       ('BuildingCode', ['2018IBC', '2021IBC'], '(AHJ.BuildingCode=%(BuildingCode0)s OR AHJ.BuildingCode=%(BuildingCode1)s) AND '),
       ('BuildingCode', ['2018IBC'], '(AHJ.BuildingCode=%(BuildingCode0)s) AND '),
       ('BuildingCode', None, ''),
   ]
)
def test_list_query_cond(type, val, expected_output):
    assert get_list_query_cond(type,val, {}) == expected_output

@pytest.mark.parametrize(
   'type, val, expected_output', [
       ('BuildingCode', '2018IBC', 'AHJ.BuildingCode=%(BuildingCode)s AND '),
       ('City', None, ''),
   ]
)
def test_get_basic_query_cond(type, val, expected_output):
    assert get_basic_query_cond(type,val, {}) == expected_output

def test_point_to_polygon_geojson(geojson_point, geojson_polygon):
    assert point_to_polygon_geojson(geojson_point) == geojson_polygon

def test_get_multipolygon__collection_exists(location, feature_collection):
    request = HttpRequest()
    request.method = 'POST'
    request.data = feature_collection
    resp = get_multipolygon(request, location)
    assert str(resp) == 'MULTIPOLYGON (((-111.7 40.97, -111.6 40.83, -111.87 40.81, -111.7 40.97)), ((1 1, 1 1, 1 1, 1 1)))'

def test_get_multipolygon__collection_does_not_exist(location):
    request = HttpRequest()
    request.data = {}
    assert get_multipolygon(request, location) == None

def test_get_multipolygon_wkt(mpoly_obj):
    assert str(get_multipolygon_wkt(mpoly_obj)) == 'MULTIPOLYGON(((0 0, 0 1, 1 1, 0 0)), ((1 1, 1 2, 2 2, 1 1)))' 

@pytest.mark.django_db
def test_order_ahj_list_AHJLevelCode_PolygonLandArea():
    ahjLevel1 = AHJLevelCode.objects.create(AHJLevelCodeID=1, Value=AHJ_LEVEL_CODE_CHOICES[0][0])
    ahjLevel2 = AHJLevelCode.objects.create(AHJLevelCodeID=2, Value=AHJ_LEVEL_CODE_CHOICES[1][0])
    ahjLevel3 = AHJLevelCode.objects.create(AHJLevelCodeID=3, Value=AHJ_LEVEL_CODE_CHOICES[2][0])

    ahj1 = create_ahj(1, 1, 200, ahjLevel1)
    ahj2 = create_ahj(2, 2, 10000, ahjLevel2)
    ahj3 = create_ahj(3, 3, 100, ahjLevel1)
    ahj4 = create_ahj(4, 4, 200, ahjLevel3)
    ahjList = [ahj1, ahj2, ahj3, ahj4]
    order_ahj_list_AHJLevelCode_PolygonLandArea(ahjList)
    assert ahjList[0].AHJPK == ahj4.AHJPK # Expected outcome: higher AHJCodeLevel comes first. If tiebreaks, lower land area comes first.
    assert ahjList[1].AHJPK == ahj2.AHJPK
    assert ahjList[2].AHJPK == ahj3.AHJPK
    assert ahjList[3].AHJPK == ahj1.AHJPK

def test_get_public_api_serializer_context():
    assert get_public_api_serializer_context() == {'is_public_view': True}

@pytest.mark.parametrize(
   'ob_json, field_name, expected_output', [
       ({ 'Building Code': {'Value' : 840}}, 'Building Code', 840), # Single value
       ({ 'Building Code': {'Value' : ['110', '50']}}, 'Building Code', ['110', '50']), # List
   ]
)
def test_get_ob_value_primitive__normal_use(ob_json, field_name, expected_output):
    assert expected_output == get_ob_value_primitive(ob_json, field_name)

def test_get_ob_value_primitive__json_incorrect_format():
    with pytest.raises(ValueError):
        assert get_ob_value_primitive({'Building Code': {}}, 'Building Code') == ''

@pytest.mark.django_db
def test_dictfetchall(create_user):
    user1 = create_user(Username='user1')
    user2 = create_user(Username='user2')
    query = "SELECT * FROM User"
    cursor = connection.cursor()
    cursor.execute(query)
    resp = dictfetchall(cursor)
    assert resp[0]['Username'] == 'user1' and resp[1]['Username'] == 'user2' # confirm both dictionaries are user objects  

# Tests for filter ahj:
# no request, no polygon or location objects
# request with no polygon or location object
# request with no polygon but has a location object (location AHJ + AHJ the match request)
# request with a polygon but no location object (all ahjs within the polygon and that match the request)
# just a polygon
# just a location

@pytest.fixture
def ahj_filter_location():
    return 'POINT(25.0, 25.0)'

@pytest.fixture
def empty_request_obj():
    request = HttpRequest()
    request.data = {}
    return request

@pytest.fixture
def ahj_filter_polygon():
    mp = MultiPolygon(geosPolygon(((0, 1), (0, 12), (10, 12), (10, 1), (0, 1))))
    return get_multipolygon_wkt(mp)

def ahj_filter_create_ahj(ahjpk, ahjid, polygonTuple, ahjLevel, BuildingCode=None, ElectricCode=None):
    p1 = geosPolygon(polygonTuple)
    mp = MultiPolygon(p1)
    polygon = Polygon.objects.create(Polygon=mp, LandArea=1, WaterArea=1, InternalPLatitude=1, InternalPLongitude=1)
    address = Address.objects.create()
    ahj = AHJ.objects.create(AHJPK=ahjpk, AHJID= ahjid, PolygonID=polygon, AddressID=address, AHJLevelCode=ahjLevel, BuildingCode=BuildingCode, ElectricCode=ElectricCode)
    StatePolygon.objects.create(PolygonID=polygon)
    return ahj

@pytest.fixture
def ahj_filter_ahjs():
    ahjLevel1 = AHJLevelCode.objects.create(AHJLevelCodeID=1, Value=AHJ_LEVEL_CODE_CHOICES[0][0])
    ahjLevel2 = AHJLevelCode.objects.create(AHJLevelCodeID=2, Value=AHJ_LEVEL_CODE_CHOICES[1][0])
    ahjLevel3 = AHJLevelCode.objects.create(AHJLevelCodeID=3, Value=AHJ_LEVEL_CODE_CHOICES[2][0])
    buildingCode = BuildingCode.objects.create(BuildingCodeID=1, Value=BUILDING_CODE_CHOICES[0][0])
    electricCode = ElectricCode.objects.create(ElectricCodeID=1, Value=ELECTRIC_CODE_CHOICES[0][0])

    ahj1 = ahj_filter_create_ahj(1, 1, ((0, 0), (0, 10), (10, 10), (10, 0), (0,0)), ahjLevel1) # AHJs 1 and 2 are in the same polygon as ahj_filter_polygon
    ahj2 = ahj_filter_create_ahj(2, 2, ((0, 3), (0, 13), (10, 13), (10, 3), (0, 3)), ahjLevel3)
    ahj3 = ahj_filter_create_ahj(3, 3, ((20, 20), (20, 30), (30, 30), (30, 20), (20,20)), ahjLevel3) # AHJ 3's polygon is over ahj_filter_location

    ahj4 = ahj_filter_create_ahj(4, 4, ((100, 100), (100, 110), (110, 110), (110, 100), (100, 100)), ahjLevel1, buildingCode, electricCode) # AHJ 4 and 5 are found through the request 
    ahj5 = ahj_filter_create_ahj(5, 5, ((100, 100), (100, 110), (110, 110), (110, 100), (100, 100)), ahjLevel1, buildingCode, electricCode)
    return ahj1, ahj2, ahj3, ahj4, ahj5

@pytest.mark.django_db
def test_filter_ahjs__no_search_parameters(ahj_filter_ahjs):
    ahj1, ahj2, ahj3, ahj4, ahj5 = ahj_filter_ahjs
    assert len(filter_ahjs()) == 5 # returns all ahjs if no filtering is done. 

@pytest.mark.django_db
def test_filter_ahjs__only_location_search(ahj_filter_ahjs, ahj_filter_location):
    ahj1, ahj2, ahj3, ahj4, ahj5 = ahj_filter_ahjs
    ahj_list = filter_ahjs(location=ahj_filter_location)

    assert len(ahj_list) == 1
    assert int(ahj_list[0].AHJID) == ahj3.AHJID

@pytest.mark.django_db
def test_filter_ahjs__only_polygon_search(ahj_filter_ahjs, ahj_filter_polygon):
    ahj1, ahj2, ahj3, ahj4, ahj5 = ahj_filter_ahjs
    ahj_list = filter_ahjs(polygon=ahj_filter_polygon)

    assert len(ahj_list) == 2 # polygon should overlap with AHJs 1 and 2
    assert all(x in [int(ahj_list[0].AHJID), int(ahj_list[1].AHJID)] for x in [ahj1.AHJID, ahj2.AHJID])

@pytest.mark.django_db
def test_filter_ahjs__only_search_filters(ahj_filter_ahjs, ahj_filter_location):
    ahj1, ahj2, ahj3, ahj4, ahj5 = ahj_filter_ahjs
    ahj_list = filter_ahjs(BuildingCode=['2021IBC'], ElectricCode=['2020NEC'])
    assert len(ahj_list) == 2 
    assert ahj_list[0].AHJPK == 4 and ahj_list[1].AHJPK == 5

@pytest.mark.django_db
def test_filter_ahjs__search_filters_and_polygon(ahj_filter_ahjs, ahj_filter_polygon):
    ahj1, ahj2, ahj3, ahj4, ahj5 = ahj_filter_ahjs
    ahj_list = filter_ahjs(AHJLevelCode='040', polygon=ahj_filter_polygon)
    assert len(ahj_list) == 1
    assert ahj_list[0].AHJPK == 1

@pytest.mark.django_db
def test_filter_ahjs__search_filters_and_location(ahj_filter_ahjs, ahj_filter_location):
    ahj1, ahj2, ahj3, ahj4, ahj5 = ahj_filter_ahjs
    ahj_list = filter_ahjs(AHJLevelCode='061', location=ahj_filter_location)
    assert len(ahj_list) == 1
    assert ahj_list[0].AHJPK == 3


@pytest.mark.django_db
def test_filter_dict_keys():
    dict_to_filter = {'key1': 'value1', 'key2': 'value2'}
    keys_to_keep = {'key1'}
    filtered_dict = filter_dict_keys(dict_to_filter, keys_to_keep)
    assert filtered_dict == {'key1': 'value1'}
