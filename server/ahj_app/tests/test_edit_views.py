import pdb
import uuid
from decimal import Decimal

from django.apps import apps
from ahj_app.models import User, Edit, Comment, AHJInspection, Contact, Address, Location, AHJ, AHJUserMaintains
from django.urls import reverse
from django.utils import timezone

import pytest
import datetime
from fixtures import create_user, ahj_obj, generate_client_with_webpage_credentials, api_client, create_minimal_obj, \
    set_obj_field, get_obj_field, get_value_or_enum_row

from ahj_app.models_field_enums import RequirementLevel, LocationDeterminationMethod

from ahj_app import views_edits


@pytest.fixture
def user_obj(create_user):
    user = create_user(Username='someone')
    return user


@pytest.fixture
def add_enums():
    RequirementLevel.objects.create(Value='ConditionallyRequired')
    RequirementLevel.objects.create(Value='Required')
    RequirementLevel.objects.create(Value='Optional')
    LocationDeterminationMethod.objects.create(Value='AddressGeocoding')
    LocationDeterminationMethod.objects.create(Value='GPS')


def edit_is_pending(edit):
    return edit.ReviewStatus == 'P' and edit.ApprovedBy is None and edit.DateEffective is None and edit.IsApplied is False


def filter_to_edit(edit_dict):
    search_dict = {k: v for k, v in edit_dict.items()}
    search_dict['DateRequested__date'] = search_dict.pop('DateRequested')
    search_dict['DateEffective__date'] = search_dict.pop('DateEffective')
    return Edit.objects.filter(**search_dict)


def check_edit_exists(edit_dict):
    return filter_to_edit(edit_dict).exists()


@pytest.mark.parametrize(
    'user_type', [
        'Admin',
        'AHJOfficial'
    ]
)
@pytest.mark.django_db
def test_edit_review__authenticated_normal_use(user_type, generate_client_with_webpage_credentials, ahj_obj):
    client = generate_client_with_webpage_credentials(Username='someone')
    user = User.objects.get(Username='someone')
    if user_type == 'Admin':
        user.is_superuser = True
        user.save()
    elif user_type == 'AHJOfficial':
        AHJUserMaintains.objects.create(UserID=user, AHJPK=ahj_obj, MaintainerStatus=True)
    edit_dict = {'ChangedBy': user, 'ApprovedBy': None,
                 'SourceTable': 'AHJ', 'SourceRow': ahj_obj.pk, 'SourceColumn': 'AHJName',
                 'OldValue': 'oldname', 'NewValue': 'newname',
                 'DateRequested': timezone.now(), 'DateEffective': None,
                 'ReviewStatus': 'P', 'EditType': 'U', 'AHJPK': ahj_obj}
    edit = Edit.objects.create(**edit_dict)
    url = reverse('edit-review')
    response = client.post(url, {'EditID': edit.EditID, 'Status': 'A'})
    assert response.status_code == 200
    edit = Edit.objects.get(EditID=edit.EditID)
    assert edit.ReviewStatus == 'A'
    assert edit.ApprovedBy == user
    tomorrow = timezone.now() + datetime.timedelta(days=1)
    assert edit.DateEffective.date() == tomorrow.date()


@pytest.mark.django_db
def test_edit_review__no_auth_normal_use(generate_client_with_webpage_credentials, ahj_obj):
    client = generate_client_with_webpage_credentials(Username='someone')
    user = User.objects.get(Username='someone')
    edit_dict = {'ChangedBy': user, 'ApprovedBy': None,
                 'SourceTable': 'AHJ', 'SourceRow': ahj_obj.pk, 'SourceColumn': 'AHJName',
                 'OldValue': 'oldname', 'NewValue': 'newname',
                 'DateRequested': timezone.now(), 'DateEffective': None,
                 'ReviewStatus': 'P', 'EditType': 'U', 'AHJPK': ahj_obj}
    edit = Edit.objects.create(**edit_dict)
    url = reverse('edit-review')
    response = client.post(url, {'EditID': edit.EditID, 'Status': 'A'})
    assert response.status_code == 403


@pytest.mark.django_db
def test_edit_review__invalid_status(generate_client_with_webpage_credentials, ahj_obj):
    client = generate_client_with_webpage_credentials(Username='someone')
    user = User.objects.get(Username='someone')
    edit_dict = {'ChangedBy': user, 'ApprovedBy': None,
                 'SourceTable': 'AHJ', 'SourceRow': ahj_obj.pk, 'SourceColumn': 'AHJName',
                 'OldValue': 'oldname', 'NewValue': 'newname',
                 'DateRequested': timezone.now(), 'DateEffective': None,
                 'ReviewStatus': 'P', 'EditType': 'U', 'AHJPK': ahj_obj}
    edit = Edit.objects.create(**edit_dict)
    url = reverse('edit-review')
    response = client.post(url, {'EditID': edit.EditID, 'Status': 'Z'})
    assert response.status_code == 400

@pytest.mark.django_db
def test_edit_review__edit_does_not_exist(generate_client_with_webpage_credentials):
    client = generate_client_with_webpage_credentials(Username='someone')
    url = reverse('edit-review')
    response = client.post(url, {'EditID': 0, 'Status': 'A'})
    assert response.status_code == 400

@pytest.mark.django_db
@pytest.mark.parametrize(
   'params', [
       ({}),
       ({'EditID': '1'}),
       ({'Status': 'A'}),
   ]
)
def test_edit_review__missing_param(params, generate_client_with_webpage_credentials):
    client = generate_client_with_webpage_credentials(Username='someone')
    url = reverse('edit-review')
    response = client.post(url, params)
    assert response.status_code == 400

@pytest.mark.django_db
def test_edit_addition__normal_use(ahj_obj, generate_client_with_webpage_credentials):
    client = generate_client_with_webpage_credentials(Username='someone')
    user = User.objects.get(Username='someone')
    AHJInspection.objects.create(AHJPK=ahj_obj, AHJInspectionName='Inspection1', TechnicianRequired=1, InspectionStatus=True)
    url = reverse('edit-addition')

    response = client.post(url, {
        'SourceTable': 'AHJInspection', 
        'AHJPK': ahj_obj.AHJPK, 
        'ParentTable': 'AHJ', 
        'ParentID': ahj_obj.AHJPK, 
        'Value': [ 
            { 'AHJInspectionName': 'NewName'}
    ]}, format='json')
    assert response.status_code == 200
    assert response.data[0]['AHJInspectionName']['Value'] == 'NewName' # confirm returned AHJInspection was updated
    edit = Edit.objects.get(AHJPK=ahj_obj.AHJPK)
    assert edit.EditType == 'A'
    assert edit.NewValue == 'True'
    assert edit.SourceRow == response.data[0]['InspectionID']['Value']
    

@pytest.mark.django_db
@pytest.mark.parametrize(
   'params', [
       ({'SourceTable': 'AHJ', 'ParentID': '1', 'ParentTable': 'AHJ'}),
       ({'AHJPK': '1', 'ParentID': '1', 'ParentTable': 'AHJ'}),
       ({'SourceTable': 'AHJ', 'AHJPK': '1', 'ParentTable': 'AHJ'}),
       ({'SourceTable': 'AHJ', 'AHJPK': '1', 'ParentID': '1'})
   ]
)
def test_edit_addition__missing_param(params, generate_client_with_webpage_credentials):
    client = generate_client_with_webpage_credentials(Username='someone')
    url = reverse('edit-addition')
    response = client.post(url, params)
    assert response.status_code == 400

@pytest.mark.django_db
def test_edit_deletion__normal_use(ahj_obj, generate_client_with_webpage_credentials):
    client = generate_client_with_webpage_credentials(Username='someone')
    user = User.objects.get(Username='someone')
    inspection = AHJInspection.objects.create(AHJPK=ahj_obj, AHJInspectionName='Inspection1', TechnicianRequired=1, InspectionStatus=True)
    url = reverse('edit-deletion')

    response = client.post(url, {
        'SourceTable': 'AHJInspection', 
        'AHJPK': ahj_obj.AHJPK, 
        'ParentTable': 'AHJ', 
        'ParentID': ahj_obj.AHJPK, 
        'Value': [ 
            inspection.InspectionID
    ]}, format='json')
    assert response.status_code == 200
    edit = Edit.objects.get(AHJPK=ahj_obj.AHJPK)
    assert edit.EditType == 'D'
    assert edit.NewValue == 'False'
    assert edit.SourceRow == response.data[0]['InspectionID']['Value']

@pytest.mark.django_db
@pytest.mark.parametrize(
   'params', [
       ({'SourceTable': 'AHJ'}),
       ({'AHJPK': '1'}),
   ]
)
def test_edit_deletion__missing_param(params, generate_client_with_webpage_credentials):
    client = generate_client_with_webpage_credentials(Username='someone')
    url = reverse('edit-deletion')
    response = client.post(url, params)
    assert response.status_code == 400


@pytest.mark.parametrize(
    'ReviewStatus, DateEffective', [
        ('A', timezone.now()),
        ('A', timezone.now() - datetime.timedelta(days=1)),
        ('A', timezone.now() + datetime.timedelta(days=1)),
        ('A', None),
        ('P', timezone.now()),
        ('D', timezone.now())
    ]
)
@pytest.mark.django_db
def test_apply_edits(ReviewStatus, DateEffective, create_user, ahj_obj):
    field_name = 'AHJName'
    old_value = 'oldname'
    new_value = 'newname'
    user = create_user()
    set_obj_field(ahj_obj, field_name, old_value)
    edit_dict = {'ChangedBy': user, 'ApprovedBy': user if DateEffective is not None else None,
                 'SourceTable': 'AHJ', 'SourceRow': ahj_obj.pk, 'SourceColumn': field_name,
                 'OldValue': old_value, 'NewValue': new_value,
                 'DateRequested': timezone.now(), 'DateEffective': DateEffective,
                 'ReviewStatus': ReviewStatus, 'IsApplied': False, 'EditType': 'U', 'AHJPK': ahj_obj}
    edit = Edit.objects.create(**edit_dict)
    views_edits.apply_edits()
    ahj = AHJ.objects.get(AHJPK=ahj_obj.AHJPK)
    is_date_effective = (DateEffective.date() == datetime.date.today()) if DateEffective is not None else False
    edit_should_apply = is_date_effective and ReviewStatus == 'A'
    edit_is_applied = getattr(ahj, field_name) == new_value
    assert edit_is_applied == edit_should_apply
    edit = Edit.objects.get(EditID=edit.EditID)
    assert edit.IsApplied == edit_should_apply


@pytest.mark.django_db
def test_edit_update__normal_use(ahj_obj, generate_client_with_webpage_credentials):
    client = generate_client_with_webpage_credentials(Username='someone')
    user = User.objects.get(Username='someone')
    inspection = AHJInspection.objects.create(AHJPK=ahj_obj, AHJInspectionName='Inspection1', TechnicianRequired=1, InspectionStatus=True)
    url = reverse('edit-update')
    input = [
        {
            'AHJPK': ahj_obj.AHJPK,
            'SourceTable': 'AHJInspection',
            'SourceRow': inspection.pk,
            'SourceColumn': 'AHJInspectionName',
            'NewValue': 'NewName'
        }
    ]
    response = client.post(url, input, format='json')
    assert response.status_code == 200
    edit = Edit.objects.get(AHJPK=ahj_obj.AHJPK) # Got newly created edit object and set it as approved
    edit.ReviewStatus = 'A'
    edit.DateEffective = timezone.now()
    edit.ApprovedBy = user
    edit.save()
    views_edits.apply_edits() # Now that it's approved, apply edits will apply it.
    Inspection = AHJInspection.objects.get(AHJPK=ahj_obj)
    assert Inspection.AHJInspectionName == 'NewName'

@pytest.mark.django_db
@pytest.mark.parametrize(
   'params', [
       ({'SourceTable': 'AHJ'}),
       ({'AHJPK': '1', 'SourceTable': 'AHJ', 'SourceRow': 'row', 'SourceColumn': 'column'}),
   ]
)
def test_edit_update__missing_param(params, generate_client_with_webpage_credentials):
    client = generate_client_with_webpage_credentials(Username='someone')
    url = reverse('edit-deletion')
    response = client.post(url, params)
    assert response.status_code == 400

@pytest.mark.django_db
def test_edit_list__normal_use(ahj_obj, generate_client_with_webpage_credentials):
    client = generate_client_with_webpage_credentials(Username='someone')
    user = User.objects.get(Username='someone')
    Edit.objects.create(EditID=1, AHJPK=ahj_obj, ChangedBy=user, EditType='A', SourceTable='AHJ', SourceColumn='BuildingCode', SourceRow='2118', DateRequested=timezone.now())
    Edit.objects.create(EditID=2, AHJPK=ahj_obj, ChangedBy=user, EditType='A', SourceTable='AHJ', SourceColumn='BuildingCode', SourceRow='2118', DateRequested=timezone.now())

    url = reverse('edit-list')
    response = client.get(url, {'AHJPK':'1'})
    assert response.status_code == 200
    assert len(response.data) == 2

@pytest.mark.django_db
def test_edit_list__missing_param(generate_client_with_webpage_credentials):
    client = generate_client_with_webpage_credentials(Username='someone')
    url = reverse('edit-list')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 0


@pytest.mark.parametrize(
    'model_name, field_name, old_value, new_value, expected_value', [
        ('AHJ', 'AHJName', 'oldname', 'newname', 'old_value'),
        ('Contact', 'FirstName', 'oldname', 'newname', 'old_value'),
        ('Address', 'Country', 'oldcountry', 'newcountry', 'old_value'),
        ('Location', 'Elevation', Decimal('0.00000000'), Decimal('10000.00000000'), 'old_value'),
        ('Location', 'LocationDeterminationMethod', '', 'AddressGeocoding', None),
        ('Location', 'LocationDeterminationMethod', 'AddressGeocoding', '', 'old_value'),
        ('EngineeringReviewRequirement', 'RequirementLevel', 'ConditionallyRequired', 'Required', 'old_value'),
        ('AHJInspection', 'FileFolderURL', 'oldurl', 'newurl', 'old_value'),
        ('FeeStructure', 'FeeStructureID', str(uuid.uuid4()), str(uuid.uuid4()), 'old_value')
    ]
)
@pytest.mark.django_db
def test_edit_revert__edit_update(model_name, field_name, old_value, new_value, create_user, ahj_obj, expected_value, create_minimal_obj, add_enums):
    user = create_user()
    obj = create_minimal_obj(model_name)
    set_obj_field(obj, field_name, new_value)
    edit_dict = {'ChangedBy': user, 'ApprovedBy': user,
                 'SourceTable': model_name, 'SourceRow': obj.pk, 'SourceColumn': field_name,
                 'OldValue': old_value, 'NewValue': new_value,
                 'DateRequested': timezone.now(), 'DateEffective': timezone.now(),
                 'ReviewStatus': 'A', 'EditType': 'U', 'AHJPK': ahj_obj}
    edit = Edit.objects.create(**edit_dict)
    assert views_edits.revert_edit(user, edit)
    edit_dict['OldValue'], edit_dict['NewValue'] = edit.NewValue, edit.OldValue
    if expected_value:
        expected_value = get_value_or_enum_row(field_name, old_value)
    assert get_obj_field(obj, field_name) == expected_value
    assert check_edit_exists(edit_dict)

@pytest.mark.django_db
def test_edit_revert__edit_pending_do_nothing(create_user, ahj_obj):
    user = create_user()
    old_value = 'oldname'
    new_value = 'newname'
    set_obj_field(ahj_obj, 'AHJName', old_value)
    edit_dict = {'ChangedBy': user, 'ApprovedBy': None,
                 'SourceTable': 'AHJ', 'SourceRow': ahj_obj.pk, 'SourceColumn': 'AHJName',
                 'OldValue': old_value, 'NewValue': new_value,
                 'DateRequested': timezone.now(), 'DateEffective': None,
                 'ReviewStatus': 'P', 'EditType': 'U', 'AHJPK': ahj_obj}
    edit = Edit.objects.create(**edit_dict)
    assert not views_edits.revert_edit(user, edit)
    edit_dict['OldValue'], edit_dict['NewValue'] = old_value, edit_dict['OldValue']
    edit_dict['ReviewStatus'] = 'A'
    edit_dict['ApprovedBy'], edit_dict['DateEffective'] = user, timezone.now()
    assert not check_edit_exists(edit_dict)
    assert Edit.objects.all().count() == 1


@pytest.mark.django_db
def test_edit_revert__current_value_is_old_value_do_nothing(create_user, ahj_obj):
    user = create_user()
    old_value = 'oldname'
    new_value = 'newname'
    set_obj_field(ahj_obj, 'AHJName', old_value)
    edit_dict = {'ChangedBy': user, 'ApprovedBy': user,
                 'SourceTable': 'AHJ', 'SourceRow': ahj_obj.pk, 'SourceColumn': 'AHJName',
                 'OldValue': old_value, 'NewValue': new_value,
                 'DateRequested': timezone.now(), 'DateEffective': timezone.now(),
                 'ReviewStatus': 'A', 'EditType': 'U', 'AHJPK': ahj_obj}
    edit = Edit.objects.create(**edit_dict)
    assert not views_edits.revert_edit(user, edit)
    edit_dict['OldValue'], edit_dict['NewValue'] = old_value, edit_dict['OldValue']
    assert not check_edit_exists(edit_dict)
    assert Edit.objects.all().count() == 1


@pytest.mark.django_db
def test_edit_revert__revert_edit_old_value_uses_current_row_value(create_user, ahj_obj):
    user = create_user()
    old_value = 'oldname'
    middle_value = 'newername'
    new_value = 'newestname'
    edit_dict = {'ChangedBy': user, 'ApprovedBy': user,
                 'SourceTable': 'AHJ', 'SourceRow': ahj_obj.pk, 'SourceColumn': 'AHJName',
                 'OldValue': old_value, 'NewValue': middle_value,
                 'DateRequested': timezone.now(), 'DateEffective': timezone.now(),
                 'ReviewStatus': 'A', 'EditType': 'U', 'AHJPK': ahj_obj}
    edit = Edit.objects.create(**edit_dict)
    edit_dict['OldValue'], edit_dict['NewValue'] = edit_dict['NewValue'], new_value
    setattr(ahj_obj, 'AHJName', new_value)
    ahj_obj.save()
    newer_edit = Edit.objects.create(**edit_dict)
    assert views_edits.revert_edit(user, edit)
    edit_dict['OldValue'], edit_dict['NewValue'] = edit_dict['NewValue'], old_value
    reverting_edit = filter_to_edit(edit_dict)
    assert reverting_edit.exists()
    assert reverting_edit.first().OldValue == new_value
    assert get_obj_field(ahj_obj, 'AHJName')


@pytest.mark.parametrize(
    'parent_model_name, model_name', [
        ('AHJ', 'Contact'),
        ('AHJInspection', 'Contact'),
        ('AHJ', 'EngineeringReviewRequirement'),
        ('AHJ', 'AHJInspection'),
        ('AHJ', 'DocumentSubmissionMethod'),
        ('AHJ', 'PermitIssueMethod'),
        ('AHJ', 'FeeStructure')
    ]
)
@pytest.mark.django_db
def test_edit_revert__edit_addition(parent_model_name, model_name, create_user, create_minimal_obj, ahj_obj):
    user = create_user()
    parent_obj = create_minimal_obj(parent_model_name)
    obj = create_minimal_obj(model_name)
    relation = obj.create_relation_to(parent_obj)
    set_obj_field(relation, relation.get_relation_status_field(), True)
    edit_dict = {'ChangedBy': user, 'ApprovedBy': user,
                 'SourceTable': relation.__class__.__name__, 'SourceRow': relation.pk, 'SourceColumn': relation.get_relation_status_field(),
                 'OldValue': None, 'NewValue': True,
                 'DateRequested': timezone.now(), 'DateEffective': timezone.now(),
                 'ReviewStatus': 'A', 'EditType': 'A', 'AHJPK': ahj_obj}
    edit = Edit.objects.create(**edit_dict)
    assert views_edits.revert_edit(user, edit)
    edit_dict['OldValue'], edit_dict['NewValue'] = edit_dict['NewValue'], False
    assert check_edit_exists(edit_dict)
    assert get_obj_field(relation, relation.get_relation_status_field()) == edit_dict['NewValue']


@pytest.mark.parametrize(
    'parent_model_name, model_name', [
        ('AHJ', 'Contact'),
        ('AHJInspection', 'Contact'),
        ('AHJ', 'EngineeringReviewRequirement'),
        ('AHJ', 'AHJInspection'),
        ('AHJ', 'DocumentSubmissionMethod'),
        ('AHJ', 'PermitIssueMethod'),
        ('AHJ', 'FeeStructure')
    ]
)
@pytest.mark.django_db
def test_edit_revert__edit_deletion(parent_model_name, model_name, create_user, create_minimal_obj, ahj_obj):
    user = create_user()
    parent_obj = create_minimal_obj(parent_model_name)
    obj = create_minimal_obj(model_name)
    relation = obj.create_relation_to(parent_obj)
    set_obj_field(relation, relation.get_relation_status_field(), False)
    edit_dict = {'ChangedBy': user, 'ApprovedBy': user,
                 'SourceTable': relation.__class__.__name__, 'SourceRow': relation.pk, 'SourceColumn': relation.get_relation_status_field(),
                 'OldValue': True, 'NewValue': False,
                 'DateRequested': timezone.now(), 'DateEffective': timezone.now(),
                 'ReviewStatus': 'A', 'EditType': 'D', 'AHJPK': ahj_obj}
    edit = Edit.objects.create(**edit_dict)
    assert views_edits.revert_edit(user, edit)
    edit_dict['OldValue'], edit_dict['NewValue'] = edit_dict['NewValue'], edit_dict['OldValue']
    assert check_edit_exists(edit_dict)
    assert get_obj_field(relation, relation.get_relation_status_field()) == edit_dict['NewValue']


@pytest.mark.parametrize(
    'edit_status1, is_applied1, is_applied2, expected_outcome', [
        # Rejected edits are resettable.
        ('R', False, True, True),
        # Approved, but not yet applied, edits are resettable.
        ('A', False, False, True),
        ('A', False, True, True),
        # Approved and applied edits where they are the latest applied are resettable.
        ('A', True, False, True),
        # Approved and applied edits where another edit was since applied are not resettable.
        ('A', True, True, False)
    ]
)
@pytest.mark.django_db
def test_edit_is_resettable(edit_status1, is_applied1, is_applied2, expected_outcome, create_user, ahj_obj):
    user = create_user()
    new_value = 'newname'
    old_value = 'oldname'
    edit_dict = {'ChangedBy': user, 'ApprovedBy': user,
                 'SourceTable': 'AHJ', 'SourceRow': ahj_obj.pk, 'SourceColumn': 'AHJName',
                 'OldValue': old_value, 'NewValue': new_value,
                 'DateRequested': timezone.now(), 'DateEffective': timezone.now(),
                 'ReviewStatus': edit_status1, 'IsApplied': is_applied1, 'EditType': 'U', 'AHJPK': ahj_obj}
    edit_to_reset = Edit.objects.create(**edit_dict)
    tomorrow = timezone.now() + datetime.timedelta(days=1)
    edit_dict['DateRequested'], edit_dict['DateEffective'] = tomorrow, tomorrow
    edit_dict['ReviewStatus'], edit_dict['IsApplied'] = 'A', is_applied2
    later_edit = Edit.objects.create(**edit_dict)
    assert expected_outcome == views_edits.edit_is_resettable(edit_to_reset)


@pytest.mark.django_db
def test_edit_make_pending(create_user, ahj_obj):
    user = create_user()
    set_obj_field(ahj_obj, 'AHJName', 'newername')
    edit_dict = {'ChangedBy': user, 'ApprovedBy': user,
                 'SourceTable': 'AHJ', 'SourceRow': ahj_obj.pk, 'SourceColumn': 'AHJName',
                 'OldValue': 'oldname', 'NewValue': 'newname',
                 'DateRequested': timezone.now(), 'DateEffective': timezone.now(),
                 'ReviewStatus': 'R', 'EditType': 'U', 'AHJPK': ahj_obj}
    edit = Edit.objects.create(**edit_dict)
    views_edits.edit_make_pending(edit)
    edit = Edit.objects.get(EditID=edit.EditID)
    assert edit_is_pending(edit)


@pytest.mark.parametrize(
    'model_name, field_name, old_value, new_value', [
        ('AHJ', 'AHJName', 'oldname', 'newname'),
        ('Contact', 'FirstName', 'oldname', 'newname'),
        ('Address', 'Country', 'oldcountry', 'newcountry'),
        ('Location', 'Elevation', Decimal('0.00000000'), Decimal('10000.00000000')),
        ('Location', 'LocationDeterminationMethod', '', 'AddressGeocoding'),
        ('Location', 'LocationDeterminationMethod', 'AddressGeocoding', ''),
        ('EngineeringReviewRequirement', 'RequirementLevel', 'ConditionallyRequired', 'Required'),
        ('AHJInspection', 'FileFolderURL', 'oldurl', 'newurl'),
        ('FeeStructure', 'FeeStructureID', str(uuid.uuid4()), str(uuid.uuid4()))
    ]
)
@pytest.mark.django_db
def test_edit_update_old_value(model_name, field_name, old_value, new_value, create_user, ahj_obj, create_minimal_obj, add_enums):
    user = create_user()
    obj = create_minimal_obj(model_name)
    edit_dict = {'ChangedBy': user, 'ApprovedBy': user,
                 'SourceTable': model_name, 'SourceRow': obj.pk, 'SourceColumn': field_name,
                 'OldValue': old_value, 'NewValue': new_value,
                 'DateRequested': timezone.now(), 'DateEffective': timezone.now(),
                 'ReviewStatus': 'A', 'EditType': 'U', 'AHJPK': ahj_obj}
    edit = Edit.objects.create(**edit_dict)
    views_edits.apply_edits(ready_edits=[edit])
    views_edits.edit_update_old_value(edit)
    edit = Edit.objects.get(EditID=edit.EditID)
    assert edit.OldValue == str(new_value)


@pytest.mark.parametrize(
    'model_name, field_name, old_value, new_value', [
        ('AHJ', 'AHJName', 'oldname', 'newname'),
        ('Contact', 'FirstName', 'oldname', 'newname'),
        ('Address', 'Country', 'oldcountry', 'newcountry'),
        ('Location', 'Elevation', Decimal('0.00000000'), Decimal('10000.00000000')),
        ('Location', 'LocationDeterminationMethod', '', 'AddressGeocoding'),
        ('Location', 'LocationDeterminationMethod', 'AddressGeocoding', ''),
        ('EngineeringReviewRequirement', 'RequirementLevel', 'ConditionallyRequired', 'Required'),
        ('AHJInspection', 'FileFolderURL', 'oldurl', 'newurl'),
        ('FeeStructure', 'FeeStructureID', str(uuid.uuid4()), str(uuid.uuid4()))
    ]
)
@pytest.mark.django_db
def test_edit_update_old_value_all_awaiting_apply_or_review(model_name, field_name, old_value, new_value, create_user, ahj_obj, create_minimal_obj, add_enums):
    user = create_user()
    obj = create_minimal_obj(model_name)
    edit_dict = {'ChangedBy': user, 'ApprovedBy': user,
                 'SourceTable': model_name, 'SourceRow': obj.pk, 'SourceColumn': field_name,
                 'OldValue': old_value, 'NewValue': new_value,
                 'DateRequested': timezone.now(), 'DateEffective': timezone.now(),
                 'ReviewStatus': 'A', 'IsApplied': True, 'EditType': 'U', 'AHJPK': ahj_obj}
    edit = Edit.objects.create(**edit_dict)
    edit_dict['IsApplied'] = False
    approved_edit = Edit.objects.create(**edit_dict)
    edit_dict['ReviewStatus'] = 'P'
    pending_edit = Edit.objects.create(**edit_dict)
    views_edits.apply_edits(ready_edits=[edit])
    views_edits.edit_update_old_value_all_awaiting_apply_or_review(edit)
    approved_edit = Edit.objects.get(EditID=approved_edit.EditID)
    pending_edit = Edit.objects.get(EditID=pending_edit.EditID)
    assert approved_edit.OldValue == str(new_value)
    assert pending_edit.OldValue == str(new_value)


@pytest.mark.parametrize(
    'model_name, field_name, old_value, new_value, expected_value', [
        ('AHJ', 'AHJName', 'oldname', 'newname', 'old_value'),
        ('Contact', 'FirstName', 'oldname', 'newname', 'old_value'),
        ('Address', 'Country', 'oldcountry', 'newcountry', 'old_value'),
        ('Location', 'Elevation', Decimal('0.00000000'), Decimal('10000.00000000'), 'old_value'),
        ('Location', 'LocationDeterminationMethod', '', 'AddressGeocoding', None),
        ('Location', 'LocationDeterminationMethod', 'AddressGeocoding', '', 'old_value'),
        ('EngineeringReviewRequirement', 'RequirementLevel', 'ConditionallyRequired', 'Required', 'old_value'),
        ('AHJInspection', 'FileFolderURL', 'oldurl', 'newurl', 'old_value'),
        ('FeeStructure', 'FeeStructureID', str(uuid.uuid4()), str(uuid.uuid4()), 'old_value')
    ]
)
@pytest.mark.django_db
def test_edit_undo_apply(model_name, field_name, old_value, new_value, create_user, ahj_obj, expected_value, create_minimal_obj, add_enums):
    user = create_user()
    obj = create_minimal_obj(model_name)
    edit_dict = {'ChangedBy': user, 'ApprovedBy': user,
                 'SourceTable': model_name, 'SourceRow': obj.pk, 'SourceColumn': field_name,
                 'OldValue': old_value, 'NewValue': new_value,
                 'DateRequested': timezone.now(), 'DateEffective': timezone.now(),
                 'ReviewStatus': 'A', 'EditType': 'U', 'AHJPK': ahj_obj}
    edit = Edit.objects.create(**edit_dict)
    views_edits.apply_edits(ready_edits=[edit])
    views_edits.edit_undo_apply(edit)
    if expected_value == 'old_value':
        expected_value = get_value_or_enum_row(field_name, old_value)
    assert get_obj_field(obj, field_name) == expected_value


@pytest.mark.parametrize(
    'model_name, field_name, old_value, new_value, expected_value', [
        ('AHJ', 'AHJName', 'oldname', 'newname', 'old_value'),
        ('Contact', 'FirstName', 'oldname', 'newname', 'old_value'),
        ('Address', 'Country', 'oldcountry', 'newcountry', 'old_value'),
        ('Location', 'Elevation', Decimal('0.00000000'), Decimal('10000.00000000'), 'old_value'),
        ('Location', 'LocationDeterminationMethod', '', 'AddressGeocoding', None),
        ('Location', 'LocationDeterminationMethod', 'AddressGeocoding', '', 'old_value'),
        ('EngineeringReviewRequirement', 'RequirementLevel', 'ConditionallyRequired', 'Required', 'old_value'),
        ('AHJInspection', 'FileFolderURL', 'oldurl', 'newurl', 'old_value'),
        ('FeeStructure', 'FeeStructureID', str(uuid.uuid4()), str(uuid.uuid4()), 'old_value')
    ]
)
@pytest.mark.django_db
def test_edit_reset__edit_update(model_name, field_name, old_value, new_value, create_user, ahj_obj, create_minimal_obj, expected_value, add_enums):
    user = create_user()
    obj = create_minimal_obj(model_name)
    set_obj_field(obj, field_name, new_value)
    edit_dict = {'ChangedBy': user, 'ApprovedBy': user,
                 'SourceTable': model_name, 'SourceRow': obj.pk, 'SourceColumn': field_name,
                 'OldValue': old_value, 'NewValue': new_value,
                 'DateRequested': timezone.now(), 'DateEffective': timezone.now(),
                 'ReviewStatus': 'A', 'IsApplied': True, 'EditType': 'U', 'AHJPK': ahj_obj}
    edit = Edit.objects.create(**edit_dict)
    assert views_edits.reset_edit(user, edit)
    assert edit_is_pending(edit)
    if expected_value == 'old_value':
        expected_value = get_value_or_enum_row(field_name, old_value)
    assert get_obj_field(obj, field_name) == expected_value


@pytest.mark.parametrize(
    'parent_model_name, model_name, review_status', [
        ('AHJ', 'Contact', 'A'),
        ('AHJInspection', 'Contact', 'A'),
        ('AHJ', 'EngineeringReviewRequirement', 'A'),
        ('AHJ', 'AHJInspection', 'A'),
        ('AHJ', 'DocumentSubmissionMethod', 'A'),
        ('AHJ', 'PermitIssueMethod', 'A'),
        ('AHJ', 'FeeStructure', 'A'),
        ('AHJ', 'Contact', 'R'),
        ('AHJInspection', 'Contact', 'R'),
        ('AHJ', 'EngineeringReviewRequirement', 'R'),
        ('AHJ', 'AHJInspection', 'R'),
        ('AHJ', 'DocumentSubmissionMethod', 'R'),
        ('AHJ', 'PermitIssueMethod', 'R'),
        ('AHJ', 'FeeStructure', 'R')
    ]
)
@pytest.mark.django_db
def test_edit_reset__edit_addition(parent_model_name, model_name, review_status, create_user, create_minimal_obj, ahj_obj):
    user = create_user()
    parent_obj = create_minimal_obj(parent_model_name)
    obj = create_minimal_obj(model_name)
    relation = obj.create_relation_to(parent_obj)
    set_obj_field(relation, relation.get_relation_status_field(), review_status == 'A')
    edit_dict = {'ChangedBy': user, 'ApprovedBy': user,
                 'SourceTable': relation.__class__.__name__, 'SourceRow': relation.pk, 'SourceColumn': relation.get_relation_status_field(),
                 'OldValue': None, 'NewValue': True,
                 'DateRequested': timezone.now(), 'DateEffective': timezone.now(),
                 'ReviewStatus': review_status, 'IsApplied': review_status == 'A', 'EditType': 'A', 'AHJPK': ahj_obj}
    edit = Edit.objects.create(**edit_dict)
    assert views_edits.reset_edit(user, edit)
    assert edit_is_pending(edit)
    assert get_obj_field(relation, relation.get_relation_status_field()) == edit_dict['OldValue']


@pytest.mark.parametrize(
    'parent_model_name, model_name, review_status', [
        ('AHJ', 'Contact', 'A'),
        ('AHJInspection', 'Contact', 'A'),
        ('AHJ', 'EngineeringReviewRequirement', 'A'),
        ('AHJ', 'AHJInspection', 'A'),
        ('AHJ', 'DocumentSubmissionMethod', 'A'),
        ('AHJ', 'PermitIssueMethod', 'A'),
        ('AHJ', 'FeeStructure', 'A'),
        ('AHJ', 'Contact', 'R'),
        ('AHJInspection', 'Contact', 'R'),
        ('AHJ', 'EngineeringReviewRequirement', 'R'),
        ('AHJ', 'AHJInspection', 'R'),
        ('AHJ', 'DocumentSubmissionMethod', 'R'),
        ('AHJ', 'PermitIssueMethod', 'R'),
        ('AHJ', 'FeeStructure', 'R')
    ]
)
@pytest.mark.django_db
def test_edit_reset__edit_deletion(parent_model_name, model_name, review_status, create_user, create_minimal_obj, ahj_obj):
    user = create_user()
    parent_obj = create_minimal_obj(parent_model_name)
    obj = create_minimal_obj(model_name)
    relation = obj.create_relation_to(parent_obj)
    set_obj_field(relation, relation.get_relation_status_field(), review_status != 'A')
    edit_dict = {'ChangedBy': user, 'ApprovedBy': user,
                 'SourceTable': relation.__class__.__name__, 'SourceRow': relation.pk, 'SourceColumn': relation.get_relation_status_field(),
                 'OldValue': True, 'NewValue': False,
                 'DateRequested': timezone.now(), 'DateEffective': timezone.now(),
                 'ReviewStatus': review_status, 'IsApplied': review_status == 'A', 'EditType': 'A', 'AHJPK': ahj_obj}
    edit = Edit.objects.create(**edit_dict)
    assert views_edits.reset_edit(user, edit)
    edit = Edit.objects.get(EditID=edit.EditID)
    assert edit_is_pending(edit)
    assert get_obj_field(relation, relation.get_relation_status_field()) == edit_dict['OldValue']


@pytest.mark.django_db
def test_edit_reset__edit_pending_do_nothing(create_user, ahj_obj):
    user = create_user()
    old_value = 'oldname'
    new_value = 'newname'
    set_obj_field(ahj_obj, 'AHJName', old_value)
    edit_dict = {'ChangedBy': user, 'ApprovedBy': None,
                 'SourceTable': 'AHJ', 'SourceRow': ahj_obj.pk, 'SourceColumn': 'AHJName',
                 'OldValue': old_value, 'NewValue': new_value,
                 'DateRequested': timezone.now(), 'DateEffective': None,
                 'ReviewStatus': 'P', 'EditType': 'U', 'AHJPK': ahj_obj}
    edit = Edit.objects.create(**edit_dict)
    assert not views_edits.reset_edit(user, edit)
    edit_dict['OldValue'], edit_dict['NewValue'] = old_value, edit_dict['OldValue']
    edit_dict['ReviewStatus'] = 'A'
    edit_dict['ApprovedBy'], edit_dict['DateEffective'] = user, timezone.now()
    assert not check_edit_exists(edit_dict)
    assert Edit.objects.all().count() == 1


@pytest.mark.parametrize(
    'force_resettable, skip_undo', [
        (True, False),
        (True, True)
    ]
)
@pytest.mark.django_db
def test_edit_reset__kwargs(force_resettable, skip_undo, create_user, ahj_obj):
    user = create_user()
    old_value = 'oldname'
    new_value = 'newname'
    later_value = 'newname_later'
    set_obj_field(ahj_obj, 'AHJName', later_value)
    edit_dict = {'ChangedBy': user, 'ApprovedBy': user,
                 'SourceTable': 'AHJ', 'SourceRow': ahj_obj.pk, 'SourceColumn': 'AHJName',
                 'OldValue': old_value, 'NewValue': new_value,
                 'DateRequested': timezone.now(), 'DateEffective': timezone.now(),
                 'ReviewStatus': 'A', 'IsApplied': True, 'EditType': 'U', 'AHJPK': ahj_obj}
    edit = Edit.objects.create(**edit_dict)
    edit_dict['OldValue'], edit_dict['NewValue'] = edit_dict['NewValue'], later_value
    later_edit = Edit.objects.create(**edit_dict)
    assert views_edits.reset_edit(user, edit, force_resettable=force_resettable, skip_undo=skip_undo)
    edit = Edit.objects.get(EditID=edit.EditID)
    if force_resettable and not skip_undo:
        assert get_obj_field(ahj_obj, 'AHJName') == old_value
    elif force_resettable and skip_undo:
        assert get_obj_field(ahj_obj, 'AHJName') == later_value
        assert edit.OldValue == later_value
    assert edit.NewValue == new_value
    assert edit_is_pending(edit)
