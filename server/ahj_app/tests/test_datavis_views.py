from django.urls import reverse
from django.contrib.gis.geos import Polygon as geosPolygon
from django.contrib.gis.geos import MultiPolygon
from ahj_app.models import AHJ, Address, Polygon, StatePolygon, CityPolygon, CountyPolygon, CountySubdivisionPolygon
from fixtures import *
import pytest
import datetime

def poly_obj(idNum):
    p1 = geosPolygon( ((0, 0), (0, 1), (1, 1), (0, 0)) )
    p2 = geosPolygon( ((1, 1), (1, 2), (2, 2), (1, 1)) )
    mp = MultiPolygon(p1, p2)
    polygon = Polygon.objects.create(PolygonID=idNum, Polygon=mp, LandArea=1, WaterArea=1, InternalPLatitude=1, InternalPLongitude=1)
    return polygon

@pytest.mark.django_db
def test_data_map__empty_param(client_with_webpage_credentials):
    polyArr = []

    for i in range(1,5): # generate 4 polygons
        polyArr.append(poly_obj(i))
    
    for i in range(0,3): # assign 3 of those polygons as state polygons
        StatePolygon.objects.create(PolygonID=polyArr[i])

    ahj = AHJ.objects.create(AHJPK=1, AHJID=1, PolygonID=polyArr[0], AddressID=Address.objects.create())
    ahj = AHJ.objects.create(AHJPK=2, AHJID=2, PolygonID=polyArr[1], AddressID=Address.objects.create())
    ahj = AHJ.objects.create(AHJPK=3, AHJID=3, PolygonID=polyArr[2], AddressID=Address.objects.create())

    url = reverse('data-map')
    response = client_with_webpage_credentials.get(url) # Get all the polygons that are a StatePolygon
    assert len(response.data) == 3 # Should be only 3 polygons that are state polygons, 1 is not a StatePolygon
    assert response.status_code == 200

@pytest.mark.django_db
def test_data_map__normal_call(client_with_webpage_credentials):
    polyArr = []
    # generate 4 polygons that we can use for the below polygon types
    for i in range(1,5):
        polyArr.append(poly_obj(i))
    statePolygon = StatePolygon.objects.create(PolygonID=polyArr[0])
    cityPoly = CityPolygon.objects.create(PolygonID=polyArr[1], StatePolygonID=statePolygon)
    countyPoly = CountyPolygon.objects.create(PolygonID=polyArr[2], StatePolygonID=statePolygon)
    countySubdivPoly = CountySubdivisionPolygon.objects.create(PolygonID=polyArr[3], StatePolygonID=statePolygon)

    url = reverse('data-map')
    response = client_with_webpage_credentials.get(url, {'StatePK':1})
    assert len(response.data) == 3 # should return the three polygon types that correspond to the StatePolygonID
    assert response.status_code == 200

@pytest.mark.django_db
def test_data_map_get_polygon__normal_call(client_with_webpage_credentials):
    polygon = poly_obj(1)

    url = reverse('data-map-polygon')
    response = client_with_webpage_credentials.get(url, {'PolygonID': 1})
    assert response.data['type'] == 'Feature' # Check that a single GeoJSON polygon was returned
    assert response.status_code == 200

@pytest.mark.django_db
def test_data_map_get_polygon__no_param_passed(client_with_webpage_credentials):
    url = reverse('data-map-polygon')
    response = client_with_webpage_credentials.get(url)
    assert response.status_code == 400

@pytest.mark.django_db
def test_data_map_get_polygon__polygon_does_not_exist(client_with_webpage_credentials):
    url = reverse('data-map-polygon')
    response = client_with_webpage_credentials.get(url, {'PolygonID': 1})
    assert response.status_code == 400