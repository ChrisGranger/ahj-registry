from django.apps import apps
from django.urls import reverse, resolve
from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon
from django.contrib.gis.geos import Polygon as geosPolygon
from ahj_app.models import WebpageToken, APIToken, User, Contact, Address, AHJ, AHJUserMaintains, Polygon
from ahj_app.utils import ENUM_FIELDS, get_enum_value_row
from rest_framework.test import APIClient
from constants import webpageTokenUrls, apiTokenUrls
import datetime
import pytest
import random
import string
import uuid


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user(db, django_user_model):
    def make_user(**kwargs):
        if 'password' not in kwargs:
            kwargs['password'] = 'strong-test-pass'
        # If any required field missing, generate it here
        if 'Username' not in kwargs or kwargs['Username'] is None:
            kwargs['Username'] = str(uuid.uuid4())
        if 'Email' not in kwargs or kwargs['Email'] is None:
            kwargs['Email'] = str(uuid.uuid4()) + '@gmail.com'
        if kwargs.get('is_superuser', False):
            user = django_user_model.objects.create_superuser(**kwargs)
        else:
            user = django_user_model.objects.create_user(**kwargs)
        User.objects.filter(UserID=user.UserID).update(is_active = True)
        return user
    return make_user

@pytest.fixture
def client_without_credentials(db, api_client):
   yield api_client

@pytest.fixture
def create_user_with_active_api_token(create_user):
    def make_user(**kwargs):
        user = create_user(**kwargs)
        user.api_token.is_active = True
        user.api_token.save()
        return user
    return make_user

@pytest.fixture
def client_with_credentials(db, create_user, api_client):
   user = create_user()
   api_client.force_authenticate(user=user)
   yield api_client
   api_client.force_authenticate(user=None)

@pytest.fixture
def client_with_webpage_credentials(db, create_user, api_client):
   user = create_user()
   token = WebpageToken.objects.create(user=user)
   api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
   return api_client

@pytest.fixture
def generate_client_with_webpage_credentials(db, create_user, api_client):
    def generate_client(**kwargs):
        username = kwargs.pop('Username', None)
        email = kwargs.pop('Email', None)
        user = create_user(Username=username, Email=email)
        token = WebpageToken.objects.create(user=user)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        return api_client
    return generate_client

@pytest.fixture
def client_with_api_credentials(db, create_user_with_active_api_token, api_client):
   user = create_user_with_active_api_token()
   api_client.credentials(HTTP_AUTHORIZATION='Token ' + user.api_token.key)
   return api_client

@pytest.fixture
def generate_client_with_api_credentials(db, create_user, api_client):
    def generate_client(**kwargs):
        username = kwargs.pop('Username', None)
        email = kwargs.pop('Email', None)
        user = create_user(Username=username, Email=email)
        token = APIToken.objects.create(user=user)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        return api_client
    return generate_client

@pytest.fixture
def ahj_obj(db):
    p1 = geosPolygon( ((0, 0), (0, 1), (1, 1), (0, 0)) )
    p2 = geosPolygon( ((1, 1), (1, 2), (2, 2), (1, 1)) )
    mp = MultiPolygon(p1, p2)
    polygon = Polygon.objects.create(Polygon=mp, LandArea=1, WaterArea=1, InternalPLatitude=1, InternalPLongitude=1)
    address = Address.objects.create()
    ahj = AHJ.objects.create(AHJPK=1, PolygonID=polygon, AddressID=address, AHJID='63e32327-7a31-4a0c-a715-20d46355cc9e')
    return ahj 

@pytest.fixture
def ahj_obj_factory(db):
    def make_ahj():
        p1 = geosPolygon( ((0, 0), (0, 1), (1, 1), (0, 0)) )
        p2 = geosPolygon( ((1, 1), (1, 2), (2, 2), (1, 1)) )
        mp = MultiPolygon(p1, p2)
        polygon = Polygon.objects.create(Polygon=mp, LandArea=1, WaterArea=1, InternalPLatitude=1, InternalPLongitude=1)
        address = Address.objects.create()
        ahj = AHJ.objects.create(AHJID=uuid.uuid4(), PolygonID=polygon, AddressID=address)
        return ahj
    return make_ahj


def create_obj_from_dict(model_name, obj_dict):
    for k, v in obj_dict.items():
        if type(v) is dict:
            sub_obj_model_name = v.pop('_model_name')
            obj_dict[k] = create_obj_from_dict(sub_obj_model_name, v)
    obj = apps.get_model('ahj_app', model_name).objects.create(**obj_dict)
    return obj


@pytest.fixture
def create_minimal_obj(db):
    def get_minimal_obj(model_name):
        minimal_dicts = {'AHJ': {'AHJID': uuid.uuid4(), 'AddressID': {'_model_name': 'Address', 'LocationID': {'_model_name': 'Location'}}},
                         'Contact': {'AddressID': {'_model_name': 'Address', 'LocationID': {'_model_name': 'Location'}}},
                         'Address': {'LocationID': {'_model_name': 'Location'}},
                         'Location': {},
                         'EngineeringReviewRequirement': {'AHJPK': {'_model_name': 'AHJ', 'AHJID': uuid.uuid4(), 'AddressID': {'_model_name': 'Address', 'LocationID': {'_model_name': 'Location'}}}},
                         'AHJInspection': {'AHJPK': {'_model_name': 'AHJ', 'AHJID': uuid.uuid4(), 'AddressID': {'_model_name': 'Address', 'LocationID': {'_model_name': 'Location'}}}},
                         'DocumentSubmissionMethod': {'Value': 'SolarApp'},
                         'PermitIssueMethod': {'Value': 'SolarApp'},
                         'FeeStructure': {'AHJPK': {'_model_name': 'AHJ', 'AHJID': uuid.uuid4(), 'AddressID': {'_model_name': 'Address', 'LocationID': {'_model_name': 'Location'}}}}}
        return create_obj_from_dict(model_name, minimal_dicts[model_name])
    return get_minimal_obj


ENUM_FIELDS = {
    'BuildingCode',
    'ElectricCode',
    'FireCode',
    'ResidentialCode',
    'WindCode',
    'AHJLevelCode',
    'DocumentSubmissionMethod',
    'PermitIssueMethod',
    'AddressType',
    'LocationDeterminationMethod',
    'LocationType',
    'ContactType',
    'PreferredContactMethod',
    'EngineeringReviewType',
    'RequirementLevel',
    'StampType',
    'FeeStructureType',
    'InspectionType'
}


@pytest.fixture
def add_enum_value_rows():
    """
    Adds all enum values to their enum tables.
    """
    for field in ENUM_FIELDS:
        model = apps.get_model('ahj_app', field)
        model.objects.all().delete()
        model.objects.bulk_create([model(Value=choice[0]) for choice in model._meta.get_field('Value').choices])


def get_value_or_enum_row(field_name, value):
    return get_enum_value_row(field_name, value) if field_name in ENUM_FIELDS else value


def get_obj_field(obj, field_name):
    return getattr(obj._meta.model.objects.get(**{obj._meta.pk.name: obj.pk}), field_name)


def set_obj_field(obj, field_name, value):
    if field_name in ENUM_FIELDS:
        if value == '':
            value = None
        else:
            value = get_enum_value_row(field_name, value)
    setattr(obj, field_name, value)
    obj.save()


@pytest.fixture
def mpoly_obj():
    p1 = geosPolygon( ((0, 0), (0, 1), (1, 1), (0, 0)) )
    p2 = geosPolygon( ((1, 1), (1, 2), (2, 2), (1, 1)) )
    mp = MultiPolygon(p1, p2)
    return mp


"""
    Fixture helper methods
"""

def random_char(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))