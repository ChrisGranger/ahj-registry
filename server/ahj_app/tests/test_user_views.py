from django.urls import reverse
from django.dispatch import receiver
from django.conf import settings
from ahj_app.models import User, Contact, AHJUserMaintains, PreferredContactMethod, WebpageToken, APIToken, SunspecAllianceMember, SunspecAllianceMemberDomain, AHJOfficeDomain
from fixtures import *
from ahj_app.signals import *
import pytest
import time

token = ''
uid = ''

@pytest.fixture
def sunspec_alliance_member():
    member = SunspecAllianceMember.objects.create(MemberID=1, MemberName='Test')
    SunspecAllianceMemberDomain.objects.create(DomainID=1, MemberID=member, Domain='test.abcd')

@pytest.fixture
def ahj_office_domain(ahj_obj):
    AHJOfficeDomain.objects.create(DomainID=1, AHJID=ahj_obj, Domain='test.abcd')

# waits for activation email's uid and token to be created abd assigns local token, uid variables
@receiver(activation_email_sent)
def user_activation_listener(sender, **kwargs):
    global uid, token
    uid = kwargs['uid']
    token = kwargs['token']

# creates a new user and returns the created uid and token sent in the activation email
def get_activation_uid_and_token(client, userData):
    response = client.post('/api/v1/auth/users/', userData)
    time.sleep(1) # wait some arbitrary time for signal receiver to get token and uid
    return token, uid

"""
    User View Endpoints
"""
@pytest.mark.django_db
def test_activate_user__user_is_not_member(generate_client_with_webpage_credentials, sunspec_alliance_member):
    client = generate_client_with_webpage_credentials(Email='f@f.femdosikf')
    token, uid = get_activation_uid_and_token(client, {'Username': 'someone', 'FirstName': 'John', 'LastName': 'Doe', 'Email': 'e@fneu.com', 'password': 'hfewdus34729'})
    
    url = reverse('user-activate')
    response = client.post(url, {'uid': uid, 'token': token})
    user = User.objects.get(Username='someone')
    assert response.status_code == 204
    assert user.MemberID == None

@pytest.mark.django_db
def test_activate_user__user_is_member(generate_client_with_webpage_credentials, sunspec_alliance_member):
    client = generate_client_with_webpage_credentials(Email='f@f.femdosikf')
    token, uid = get_activation_uid_and_token(client, {'Username': 'someone', 'FirstName': 'John', 'LastName': 'Doe', 'Email': 'e@test.abcd', 'password': 'hfewdus34729'})
    
    url = reverse('user-activate')
    response = client.post(url, {'uid': uid, 'token': token})
    user = User.objects.get(Username='someone')
    assert response.status_code == 204
    assert user.MemberID.MemberID == 1

@pytest.mark.django_db
def test_activate_user__user_is_not_ahj_maintainer(generate_client_with_webpage_credentials, ahj_office_domain):
    client = generate_client_with_webpage_credentials(Email='f@f.femdosikf')
    token, uid = get_activation_uid_and_token(client, {'Username': 'someone', 'FirstName': 'John', 'LastName': 'Doe', 'Email': 'e@fneu.com', 'password': 'hfewdus34729'})
    
    url = reverse('user-activate')
    response = client.post(url, {'uid': uid, 'token': token})
    user = User.objects.get(Username='someone')
    assert response.status_code == 204
    assert AHJUserMaintains.objects.filter(UserID=user.UserID).count() == 0

@pytest.mark.django_db
def test_activate_user__user_is_ahj_maintainer(generate_client_with_webpage_credentials, ahj_office_domain):
    client = generate_client_with_webpage_credentials(Email='f@f.femdosikf')
    token, uid = get_activation_uid_and_token(client, {'Username': 'someone', 'FirstName': 'John', 'LastName': 'Doe', 'Email': 'e@test.abcd', 'password': 'hfewdus34729'})
    
    url = reverse('user-activate')
    response = client.post(url, {'uid': uid, 'token': token})
    user = User.objects.get(Username='someone')
    assert response.status_code == 204
    assert AHJUserMaintains.objects.filter(UserID=user.UserID).count() == 1


def register_user_dict():
    return {'FirstName': 'first', 'MiddleName': 'middle', 'LastName': 'last',
            'Title': 'title', 'Email': 'email@email.email', 'WorkPhone': '123-456-7890',
            'PreferredContactMethod': 'Email', 'ContactTimezone': 'PST',
            'Username': 'username', 'password': '#$()asdf!@{}1'}


@pytest.mark.parametrize(
    'fields_to_set, response_code', [
        ({}, 201),
        ({'MiddleName': '', 'Title': '', 'WorkPhone': '', 'PreferredContactMethod': '', 'ContactTimezone': ''}, 201),
        ({'FirstName': ''}, 400),
        ({'LastName': ''}, 400),
        ({'Email': ''}, 400),
        ({'Username': ''}, 400),
        ({'password': ''}, 400)
    ]
)
@pytest.mark.django_db
def test_register_user(fields_to_set, response_code, api_client, add_enum_value_rows):
    user_dict = register_user_dict()
    for k, v in fields_to_set.items():
        user_dict[k] = v
    url = reverse('djoser:user-list')
    response = api_client.post(url, user_dict, format='json')
    assert response.status_code == response_code
    if response_code == 201:
        result = response.data
        user_fields_to_match = {*result.keys()}.intersection(user_dict.keys())
        contact_fields_to_match = {*result['ContactID'].keys()}.intersection(user_dict.keys())
        assert all(user_dict[field] == result[field] for field in user_fields_to_match)
        assert all(user_dict[field] == result['ContactID'][field]['Value'] for field in contact_fields_to_match)
        user = User.objects.get(UserID=result['UserID'])
        assert user.is_active is False
        api_token = APIToken.objects.get(user=user)
        assert api_token.is_active is False
        assert api_token.expires is None


@pytest.mark.django_db
def test_register_user__missing_fields(api_client, add_enum_value_rows):
    user_dict = register_user_dict()
    url = reverse('djoser:user-list')
    for field in user_dict.keys():
        response = api_client.post(url, {k: v for k, v in user_dict.items() if k != field}, format='json')
        assert response.status_code == 400


@pytest.mark.django_db
def test_get_active_user(client_with_webpage_credentials):
    url = reverse('active-user-info')
    response = client_with_webpage_credentials.get(url)
    assert response.status_code == 200


@pytest.mark.parametrize(
    'is_viewing_self', [
        True,
        False
    ]
)
@pytest.mark.django_db
def test_get_single_user__user_exists(is_viewing_self, create_user, generate_client_with_webpage_credentials):
    client = generate_client_with_webpage_credentials(Username='someone')
    if is_viewing_self:
        user_to_view = User.objects.get(Username='someone')
    else:
        user_to_view = create_user()
    url = reverse('single-user-info', kwargs={'username': user_to_view.Username})
    response = client.get(url)
    assert response.status_code == 200
    if is_viewing_self:
        for field in User.SERIALIZER_EXCLUDED_FIELDS:
            assert field in response.data
    else:
        for field in User.SERIALIZER_EXCLUDED_FIELDS:
            assert field not in response.data


@pytest.mark.django_db
def test_get_single_user__user_does_not_exist(generate_client_with_webpage_credentials):
    client = generate_client_with_webpage_credentials(Username='someone')
    url = reverse('single-user-info', kwargs={'username': 'test'})
    response = client.get(url)
    assert response.status_code == 400

@pytest.mark.django_db
def test_update_user__user_exists(generate_client_with_webpage_credentials, create_user):
    admin_user = create_user()
    admin_token = WebpageToken.objects.create(user_id=admin_user.UserID)
    settings.WEBPAGE_TOKEN_CONSTANT = admin_token.key
    PreferredContactMethod.objects.create(PreferredContactMethodID=1, Value='Email') # create a PreferredContactMethod so we can change that attr in the Contact model
    client = generate_client_with_webpage_credentials(Username='someone', Email='test@test.com')
    newUserData = {
        'Username': 'username',
        'FirstName': 'first',
        'LastName': 'last',
        'PersonalBio': 'pb',
        'URL': 'url',
        'CompanyAffiliation': 'ca',
        'WorkPhone': '123-456-7890',
        'PreferredContactMethod': 'Email',
        'Title': 'title'
    }
    # send update to user-update path 
    url = reverse('user-update')
    response = client.post(url, newUserData)
    # Update contact and user objects
    user = User.objects.get(Username='username')
    ContactID = user.ContactID
    # For each field in the User and Contact objects that match a field in newUserData, see if it was updated.
    for field in User._meta.get_fields():
        if field.name in newUserData:
            assert getattr(user, field.name) == newUserData[field.name]
    for field in Contact._meta.get_fields():
        if field.name in newUserData:
            if field.name == 'PreferredContactMethod':
                assert getattr(ContactID, 'PreferredContactMethod').Value == newUserData[field.name]
            else:
                assert getattr(ContactID, field.name) == newUserData[field.name]
    
    assert response.status_code == 200


@pytest.mark.parametrize(
    'is_admin, token_exists', [
        (True, True),
        (True, False),
        (False, True),
        (False, False)
    ]
)
@pytest.mark.django_db
def test_create_api_token(is_admin, token_exists, generate_client_with_webpage_credentials):
    client = generate_client_with_webpage_credentials(Username='someone')
    User.objects.filter(Username='someone').update(is_superuser=is_admin)
    url = reverse('create-api-token')
    response = client.get(url)
    if token_exists:
        response = client.get(url)
    assert response.status_code == (201 if is_admin else 403)


@pytest.mark.parametrize(
    'is_admin, already_maintains', [
        (True, True),
        (True, False),
        (False, True),
        (False, False)
    ]
)
@pytest.mark.django_db
def test_set_ahj_maintainer(is_admin, already_maintains, ahj_obj, generate_client_with_webpage_credentials):
    client = generate_client_with_webpage_credentials(Username='someone')
    User.objects.filter(Username='someone').update(is_superuser=is_admin)
    user = User.objects.get(Username='someone')

    if already_maintains:
        AHJUserMaintains.objects.create(AHJPK=ahj_obj, UserID=user, MaintainerStatus=True)
    
    userData = {'Username': user.Username, 'AHJPK': ahj_obj.AHJPK}
    url = reverse('ahj-set-maintainer')
    response = client.post(url, userData)
    assert response.status_code == (200 if is_admin else 403)


@pytest.mark.django_db
def test_set_ahj_maintainer__invalid_params(generate_client_with_webpage_credentials):
    client = generate_client_with_webpage_credentials(Username='someone')
    User.objects.filter(Username='someone').update(is_superuser=True)
    # invalid username
    userData = {'Username': 'notexist'}
    url = reverse('ahj-set-maintainer')
    response = client.post(url, userData)
    assert response.status_code == 400
    # invalid AHJPK
    userData = {'Username': 'someone', 'AHJPK': 999999999}
    url = reverse('ahj-set-maintainer')
    response = client.post(url, userData)
    assert response.status_code == 400


@pytest.mark.parametrize(
    'is_admin, already_maintains', [
        (True, True),
        (True, False),
        (False, True),
        (False, False)
    ]
)
@pytest.mark.django_db
def test_remove_ahj_maintainer(is_admin, already_maintains, ahj_obj, generate_client_with_webpage_credentials):
    client = generate_client_with_webpage_credentials(Username='someone')
    User.objects.filter(Username='someone').update(is_superuser=is_admin)
    user = User.objects.get(Username='someone')

    if already_maintains:
        AHJUserMaintains.objects.create(AHJPK=ahj_obj, UserID=user, MaintainerStatus=True)

    userData = {'Username': 'someone', 'AHJPK': ahj_obj.AHJPK}
    url = reverse('ahj-remove-maintainer')
    response = client.post(url, userData)
    if is_admin:
        assert response.status_code == 200
        if already_maintains:
            assert AHJUserMaintains.objects.get(UserID=user.UserID).MaintainerStatus is False
    else:
        assert response.status_code == 403


@pytest.mark.django_db
def test_remove_ahj_maintainer__invalid_params(generate_client_with_webpage_credentials):
    client = generate_client_with_webpage_credentials(Username='someone')
    User.objects.filter(Username='someone').update(is_superuser=True)
    # invalid username
    userData = {'Username': 'notexist'}
    url = reverse('ahj-remove-maintainer')
    response = client.post(url, userData)
    assert response.status_code == 400
    # invalid AHJPK
    userData = {'Username': 'someone', 'AHJPK': 999999999}
    url = reverse('ahj-remove-maintainer')
    response = client.post(url, userData)
    assert response.status_code == 400
