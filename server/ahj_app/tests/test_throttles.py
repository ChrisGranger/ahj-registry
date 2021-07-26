from fixtures import *
from ahj_app.models import SunspecAllianceMember, SunspecAllianceMemberDomain, User
from django.urls import reverse
import pytest
from django.conf import settings
import random
import string


@pytest.fixture
def generate_sunspec_alliance_member():
    letters = string.ascii_letters
    member = SunspecAllianceMember.objects.create(MemberName=''.join(random.choice(letters) for i in range(6)))
    domain = ''.join(random.choice(letters) for i in range(4)) + '.' + ''.join(random.choice(letters) for i in range(4))
    SunspecAllianceMemberDomain.objects.create(DomainID=1, MemberID=member, Domain=domain)
    return member.MemberID, domain

"""
    MemberRateThrottle
"""
@pytest.mark.parametrize(
   'urlName, args', [
       ('ahj-public', {'Location': {'Longitude': {'Value': -120}, 'Latitude': {'Value': 37}}}), # pass invalid args to each so early exit
       ('ahj-geo-address', {'AddrLine1': {'Value': '1600 Pennsylvania Avenue NW'}, 'City': {'Value': 'Washington'}, 'County': {'Value': 'DC'}, 'StateProvince': {'Value': 'DC'}})
   ]
)
@pytest.mark.django_db
def test_member_rate_throttle__regular_user(urlName, args, generate_client_with_api_credentials, generate_sunspec_alliance_member):
    memberID, domain = generate_sunspec_alliance_member
    client = generate_client_with_api_credentials(Email=f'f@{domain}')
    User.objects.filter(Email=f'f@{domain}').update(MemberID=memberID)
    url = reverse(urlName)
    # Test with a throttle rate that is less than actual (actual rate would take insanely long to test)
    iterNum = 5
    settings.REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']['member'] = f'{iterNum}/day'
    for _ in range(iterNum):
        response = client.post(url, args, format='json')
        assert response.status_code == 200
    response = client.post(url, args, format='json')
    assert response.status_code == 429
    assert response.data['detail'][0:22] == 'Request was throttled.'

@pytest.mark.parametrize(
   'urlName, args', [
       ('ahj-public', {'Location': {'Longitude': {'Value': 'hello'}, 'Latitude': {'Value': 'hello'}}}), # pass invalid args to each so early exit
       ('ahj-geo-address', {}),
       ('ahj-geo-location', {'Latitude': {'V': '25'}}),
   ]
)
@pytest.mark.django_db
def test_member_rate_throttle__regular_user_hits_throttle_with_bad_requests(urlName, args, generate_client_with_api_credentials, generate_sunspec_alliance_member):
    memberID, domain = generate_sunspec_alliance_member
    client = generate_client_with_api_credentials(Email=f'f@{domain}')
    User.objects.filter(Email=f'f@{domain}').update(MemberID=memberID)
    url = reverse(urlName)
    iterNum = 5
    settings.REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']['member'] = f'{iterNum}/day'
    for _ in range(iterNum):
        response = client.post(url, args, format='json')
        assert response.status_code == 400
    response = client.post(url, args, format='json')
    assert response.status_code == 429
    assert response.data['detail'][0:22] == 'Request was throttled.'

"""
    WebpageSearchThrottle
"""
@pytest.mark.django_db
def test_webpage_search_throttle__anon_user(client_without_credentials):
    url = reverse('ahj-private')
    iterNum = 3
    settings.REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']['webpage-search'] = f'{iterNum}/day'
    for _ in range(iterNum):
        response = client_without_credentials.post(url, {}, format='json')
        assert response.status_code == 200
    response = client_without_credentials.post(url, {}, format='json')
    assert response.status_code == 429
    assert response.data['detail'][0:22] == 'Request was throttled.'

@pytest.mark.django_db
def test_webpage_search_throttle__logged_in_user(generate_client_with_webpage_credentials):
    client = generate_client_with_webpage_credentials(Email='f@f.fewbudsj')
    url = reverse('ahj-private')
    iterNum = 3
    settings.REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']['webpage-search'] = f'{iterNum}/day'
    for _ in range(iterNum):
        response = client.post(url, {}, format='json')
        assert response.status_code == 200
    response = client.post(url, {}, format='json')
    assert response.status_code == 429
    assert response.data['detail'][0:22] == 'Request was throttled.'

@pytest.mark.django_db
def test_webpage_search_throttle__member_user_unlimited_requests(generate_client_with_webpage_credentials, generate_sunspec_alliance_member):
    memberID, domain = generate_sunspec_alliance_member
    client = generate_client_with_webpage_credentials(Email=f'f@{domain}')
    User.objects.filter(Email=f'f@{domain}').update(MemberID=memberID)
    url = reverse('ahj-private')
    iterNum = 3
    settings.REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']['webpage-search'] = f'{iterNum}/day'
    for _ in range(iterNum):
        response = client.post(url, {}, format='json')
        assert response.status_code == 200
    response = client.post(url, {}, format='json')
    assert response.status_code == 200
