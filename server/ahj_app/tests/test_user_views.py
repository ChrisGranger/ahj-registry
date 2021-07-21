from django.urls import reverse
from ahj_app.models import User, Contact, AHJUserMaintains, PreferredContactMethod, WebpageToken
from fixtures import *
import pytest
from django.conf import settings

"""
    User View Endpoints
"""

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
