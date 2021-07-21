from django.contrib.auth import hashers
from django.http import QueryDict
import ahj_app.admin.actions as admin_actions
import ahj_app.admin.form as admin_form
from django.utils import timezone

from fixtures import *
import pytest
import datetime

from ahj_app.models import AHJ, User, APIToken, AHJUserMaintains, Edit, Location, Address
from ahj_app.models_field_enums import LocationDeterminationMethod

from ahj_app.views_edits import apply_edits


@pytest.mark.django_db
def test_get_value_or_primary_key():
    ldm = LocationDeterminationMethod.objects.create(Value='GPS')
    location = Location.objects.create(Description='desc', LocationDeterminationMethod=ldm)
    address = Address.objects.create(LocationID=location)
    assert admin_actions.get_value_or_primary_key(location, 'Description') == 'desc'
    assert admin_actions.get_value_or_primary_key(location, 'LocationDeterminationMethod') == 'GPS'
    assert admin_actions.get_value_or_primary_key(address, 'LocationID') == location.LocationID
    assert admin_actions.get_value_or_primary_key(address, 'AddressType') == ''


@pytest.mark.parametrize(
    'password', [
        ('new_user_password')
    ]
)
@pytest.mark.django_db
def test_reset_password(password, create_user):
    user = create_user()
    admin_actions.reset_password(user, password)
    salt = user.password.split('$')[2]
    assert hashers.make_password(password, salt) == user.password


@pytest.mark.django_db
def test_partition_by_field_users_by_api_token(create_user, create_user_with_api_token):
    for x in range(0, 10):
        if x % 2 == 0:
            create_user()
        else:
            create_user_with_api_token()
    user_queryset = User.objects.all()
    those_with_field_value, those_without_field_value = admin_actions.partition_by_field(user_queryset, 'api_token', None)
    assert None in those_with_field_value.values_list('api_token', flat=True)
    assert None not in those_without_field_value.values_list('api_token', flat=True)


@pytest.mark.django_db
def test_process_generate_api_token_data(create_user):
    form_prefix = 'form-{0}'
    post_data_dict = {}
    post_query_dict = dict_make_query_dict(post_data_dict)
    users = []
    dates = []
    for x in range(5):
        user = create_user()
        date = timezone.now() + datetime.timedelta(days=x)
        date_strs = str(date.date()).split('-')
        post_query_dict.update({'user_to_form': f'{user.UserID}.{form_prefix.format(x)}',
                                f'{form_prefix.format(x)}-ExpirationDate_year': date_strs[0],
                                f'{form_prefix.format(x)}-ExpirationDate_month': date_strs[1],
                                f'{form_prefix.format(x)}-ExpirationDate_day': date_strs[2]})
        users.append(user)
        dates.append(date)
    results = admin_actions.process_generate_api_token_data(post_query_dict)
    for x in range(len(users)):
        assert results[x]['user'].UserID == users[x].UserID
        assert results[x]['expires'].date() == dates[x].date()


@pytest.mark.parametrize(
    'form_value, expected_output', [
        ('On', True),
        ('Off', False),
        ('DoNothing', None)
    ]
)
def test_set_toggle(form_value, expected_output):
    assert admin_actions.set_toggle(form_value) == expected_output


@pytest.mark.parametrize(
    'form_value, expected_output', [
        ('on', True),
        ('off', False),
        ('other_value', False)
    ]
)
def test_set_delete(form_value, expected_output):
    assert admin_actions.set_delete(form_value) == expected_output


@pytest.mark.parametrize(
    'delete', [
        True,
        False,
        None
    ]
)
@pytest.mark.django_db
def test_delete_toggle_api_token_is_deleted(delete, create_user_with_api_token):
    user = create_user_with_api_token()
    admin_actions.delete_toggle_api_token(user, delete=delete)
    assert APIToken.objects.filter(user=user).exists() != (delete if delete is not None else False)


@pytest.mark.parametrize(
    'toggle', [
        True,
        False,
        None
    ]
)
@pytest.mark.django_db
def test_delete_toggle_api_token_is_toggled(toggle, create_user_with_api_token):
    user = create_user_with_api_token()
    admin_actions.delete_toggle_api_token(user, toggle=toggle)
    assert APIToken.objects.get(user=user).is_active == (toggle if toggle is not None else True)


@pytest.mark.django_db
def test_delete_toggle_api_token_user_has_no_api_token(create_user):
    user = create_user()
    if hasattr(user, 'api_token'):
        user.api_token.delete()
    admin_actions.delete_toggle_api_token(user, toggle=True, delete=False)
    assert not APIToken.objects.filter(user=user).exists()


def dict_make_query_dict(given_dict):
    qd = QueryDict('', mutable=True)
    qd.update(given_dict)
    return qd


@pytest.mark.parametrize(
    'expect_toggle, expect_delete', [
        (None, None),
        (None, True),
        (None, False),
        (True, None),
        (True, True),
        (True, False),
        (False, None),
        (False, True),
        (False, False)
    ]
)
@pytest.mark.django_db
def test_process_delete_toggle_api_token_data(expect_toggle, expect_delete, create_user):
    if expect_toggle:
        toggle_text = 'On'
    elif expect_toggle is False:
        toggle_text = 'Off'
    else:
        toggle_text = 'DoNothing'
    if expect_delete:
        delete_text = 'on'
    else:
        delete_text = ''
    users = []
    form_prefix = 'form-{0}'
    post_data_dict = {}
    post_query_dict = dict_make_query_dict(post_data_dict)
    for x in range(5):
        user = create_user()
        users.append(user)
        post_query_dict.update({'user_to_form': f'{user.UserID}.{form_prefix.format(x)}',
                                f'{form_prefix.format(x)}-toggle': toggle_text,
                                f'{form_prefix.format(x)}-delete_token': delete_text})
    results = admin_actions.process_delete_toggle_api_token_data(post_query_dict)
    for x in range(len(users)):
        assert results[x]['user'].UserID == users[x].UserID
        assert results[x]['toggle'] == expect_toggle
        assert results[x]['delete'] == (expect_delete if expect_delete is not None else False)


@pytest.mark.parametrize(
    'num_existing, num_kept, num_new', [
        # Remove all
        (3, 0, 0),
        # Keep all
        (3, 3, 0),
        # Add all new
        (0, 0, 3),
        # Remove one
        (3, 2, 0),
        # Remove one, add new one
        (3, 2, 1),
        # Add one
        (2, 2, 1)
    ]
)
@pytest.mark.django_db
def test_assign_ahj_official_status(num_existing, num_kept, num_new, ahj_obj_factory, create_user):
    """
    num_existing: number of AHJs a user is an AHJ Official of
    num_kept: number of AHJs a user is still an AHJ Official of
    num_new: number of AHJs a user is newly assigned as an AHJ Official of
    """
    user = create_user()
    num_existing_ahjs = []
    num_kept_ahjs = []
    num_new_ahjs = []

    # Add the starting relations for what the user is an AHJ Official of
    for x in range(num_existing):
        ahj = ahj_obj_factory()
        num_existing_ahjs.append(ahj)
        AHJUserMaintains.objects.create(UserID=user, AHJPK=ahj, MaintainerStatus=True)
    # Track what AHJs the user will should still be an AHJ Official of
    for x in range(num_kept):
        num_kept_ahjs.append(num_existing_ahjs[x])
    # Track the AHJs the user is newly assigned to be an AHJ Official of
    for x in range(num_new):
        ahj = ahj_obj_factory()
        num_new_ahjs.append(ahj)

    # Test applying the changes
    admin_form.assign_ahj_official_status(user, num_kept_ahjs + num_new_ahjs)

    all_time_assigned_ahjs = AHJUserMaintains.objects.filter(UserID=user)
    assigned_ahjs = all_time_assigned_ahjs.filter(MaintainerStatus=True).values_list('AHJPK', flat=True)
    former_ahjs = all_time_assigned_ahjs.filter(MaintainerStatus=False).values_list('AHJPK', flat=True)
    for ahj in num_kept_ahjs + num_new_ahjs:
        assert ahj.AHJPK in assigned_ahjs
    for ahj in (num_existing_ahjs[num_kept:] if num_kept < len(num_existing_ahjs) else []):
        assert ahj.AHJPK in former_ahjs


@pytest.mark.django_db
def test_assign_ahj_official_status__reassign_ahj(create_user, ahj_obj):
    user = create_user()
    assignment = AHJUserMaintains.objects.create(UserID=user, AHJPK=ahj_obj, MaintainerStatus=False)
    admin_form.assign_ahj_official_status(user, [ahj_obj])
    assignment = AHJUserMaintains.objects.get(MaintainerID=assignment.MaintainerID)
    assert assignment.MaintainerStatus is True


@pytest.mark.parametrize(
    'date_str', [
        str(timezone.now()),
        str(timezone.make_aware(datetime.datetime(1, 1, 1))),
        ''
    ]
)
@pytest.mark.django_db
def test_set_date_from_str(date_str):
    try:
        date = timezone.make_aware(datetime.datetime.strptime(date_str, '%Y-%m-%d'))
    except ValueError:
        date = None
    result = admin_actions.set_date_from_str(date_str)
    assert result == date


@pytest.mark.parametrize(
    'date_effective', [
        timezone.now(),
        timezone.now() + datetime.timedelta(days=1),
        timezone.make_aware(datetime.datetime(1, 1, 1))
    ]
)
@pytest.mark.django_db
def test_process_approve_edits_data(date_effective, create_user, ahj_obj):
    form_prefix = 'form-{0}'
    post_data_dict = {}
    post_query_dict = dict_make_query_dict(post_data_dict)
    edits = []
    approving_user = create_user()
    for x in range(5):
        user = create_user()
        edit = Edit.objects.create(AHJPK=ahj_obj, ChangedBy=user, EditType='A', SourceTable='AHJ',
                                   SourceColumn='BuildingCode', SourceRow=ahj_obj.pk,
                                   DateRequested=timezone.now())
        edits.append(edit)
        date_strs = str(date_effective.date()).split('-')
        post_query_dict.update({'edit_to_form': f'{edit.EditID}.{form_prefix.format(x)}',
                                f'{form_prefix.format(x)}-DateEffective_year': date_strs[0],
                                f'{form_prefix.format(x)}-DateEffective_month': date_strs[1],
                                f'{form_prefix.format(x)}-DateEffective_day': date_strs[2]})
    results = admin_actions.process_approve_edits_data(post_query_dict, approving_user)
    for x in range(len(edits)):
        assert results[x]['edit'].EditID == edits[x].EditID
        assert results[x]['approved_by'].UserID == approving_user.UserID
        if date_effective <= timezone.now():
            date_effective = timezone.now()
        assert results[x]['date_effective'].date() == date_effective.date()
        assert results[x]['apply_now'] == (date_effective.date() == datetime.date.today())


@pytest.mark.django_db
def test_process_approve_edits_data_invalid_date_effective(create_user, ahj_obj):
    form_prefix = 'form-{0}'
    post_data_dict = {}
    post_query_dict = dict_make_query_dict(post_data_dict)
    edits = []
    approving_user = create_user()
    for x in range(5):
        user = create_user()
        edit = Edit.objects.create(AHJPK=ahj_obj, ChangedBy=user, EditType='U', SourceTable='AHJ',
                                   SourceColumn='AHJName', SourceRow=ahj_obj.pk, NewValue='NewName',
                                   DateRequested=timezone.now())
        edits.append(edit)
        post_query_dict.update({'edit_to_form': f'{edit.EditID}.{form_prefix.format(x)}',
                                f'{form_prefix.format(x)}-DateEffective_year': '',
                                f'{form_prefix.format(x)}-DateEffective_month': '',
                                f'{form_prefix.format(x)}-DateEffective_day': ''})
    results = admin_actions.process_approve_edits_data(post_query_dict, approving_user)
    assert len(results) == 0


@pytest.mark.parametrize(
    'apply_now', [
        True,
        False
    ]
)
@pytest.mark.django_db
def test_approve_edit(apply_now, create_user, ahj_obj):
    user = create_user()
    edit = Edit.objects.create(AHJPK=ahj_obj, ChangedBy=user, EditType='U', SourceTable='AHJ',
                               SourceColumn='AHJName', SourceRow=ahj_obj.pk, NewValue='NewName',
                               DateRequested=timezone.now())
    admin_actions.approve_edit(edit, user, timezone.now(), apply_now)
    edit = Edit.objects.get(EditID=edit.EditID)
    ahj = AHJ.objects.get(AHJPK=ahj_obj.pk)
    assert edit.ApprovedBy.UserID == user.UserID
    assert edit.DateEffective.date() == datetime.date.today()
    assert edit.ReviewStatus == 'A'
    if apply_now:
        assert ahj.AHJName == 'NewName'
    else:
        ahj = AHJ.objects.get(AHJPK=ahj_obj.pk)
        assert ahj.AHJName != 'NewName'
        # NOTE: apply_edits is tested separately in test_view_edits.py
        apply_edits()
        ahj = AHJ.objects.get(AHJPK=ahj_obj.pk)
        assert ahj.AHJName == 'NewName'


@pytest.mark.django_db
def test_build_url_parameters_for_change_list_filtering(ahj_obj_factory):
    ahj1 = ahj_obj_factory()
    ahj2 = ahj_obj_factory()
    ahj3 = ahj_obj_factory()
    assert admin_actions.build_url_parameters_for_change_list_filtering(AHJ.objects.all(), [admin_actions.field_key_pair('AHJPK', 'AHJPK')]) == f'?AHJPK={ahj1.pk},{ahj2.pk},{ahj3.pk}&'
