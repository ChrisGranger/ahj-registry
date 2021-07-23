import datetime

from django.apps import apps
from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .authentication import WebpageTokenAuth

from .models import AHJ, Edit, Location, AHJUserMaintains
from .serializers import AHJSerializer, EditSerializer, ContactSerializer, \
    EngineeringReviewRequirementSerializer, PermitIssueMethodUseSerializer, DocumentSubmissionMethodUseSerializer, \
    FeeStructureSerializer, AHJInspectionSerializer
from .utils import get_elevation, get_enum_value_row, get_enum_value_row_else_null, ENUM_FIELDS


def add_edit(edit_dict: dict, ReviewStatus='P', ApprovedBy=None, DateEffective=None):
    """
    Saves a new edit given a dict with these key-value pairs.
    The kwargs allow saving an approved or rejected edit.
    """
    edit = Edit()
    edit.ChangedBy = edit_dict.get('User')
    edit.DateRequested = timezone.now()
    edit.AHJPK = edit_dict.get('AHJPK')
    edit.SourceTable = edit_dict.get('SourceTable')
    edit.SourceColumn = edit_dict.get('SourceColumn')
    edit.SourceRow = edit_dict.get('SourceRow')
    edit.OldValue = edit_dict.get('OldValue')
    edit.NewValue = edit_dict.get('NewValue')
    edit.ReviewStatus = ReviewStatus
    if ReviewStatus == 'A':
        edit.ApprovedBy = ApprovedBy
        edit.DateEffective = DateEffective
    edit.EditType = edit_dict.get('EditType')
    edit.save()
    return edit


def create_addr_string(Address):
    """
    Creates a string from an Address row instance.

    :param Address: Address row instance
    :return: The address as a string
    """
    addr = Address.AddrLine1
    if addr != '' and Address.AddrLine2 != '':
        addr += ', ' + Address.AddrLine2
    elif Address.AddrLine2 != '':
        addr += Address.AddrLine2
    if addr != '' and Address.AddrLine3!= '':
        addr += ', ' + Address.AddrLine3
    elif Address.AddrLine3 != '':
        addr += Address.AddrLine3
    if addr != '' and Address.City != '':
        addr += ', ' + Address.City
    elif Address.City != '':
        addr += Address.City
    if addr != '' and Address.County != '':
        addr += ', ' + Address.County
    elif Address.County != '':
        addr += Address.County
    if addr != '' and Address.StateProvince != '':
        addr += ', ' + Address.StateProvince
    elif Address.StateProvince != '':
        addr += Address.StateProvince
    if addr != '' and Address.Country != '':
        addr += ', ' + Address.Country
    elif Address.Country != '':
        addr += Address.Country
    if addr != '' and Address.ZipPostalCode != '':
        addr += ', ' + Address.ZipPostalCode
    elif Address.ZipPostalCode != '':
        addr += Address.ZipPostalCode

    return addr


def addr_string_from_dict(Address):
    """
    Creates a string from a dict.

    :param Address: A dict containing Address model key-value pairs
    :return: The address as a string
    """
    addr = Address["AddrLine1"]
    if addr != '' and Address["AddrLine2"] != '':
        addr += ', ' + Address["AddrLine2"]
    elif Address["AddrLine2"] != '':
        addr += Address["AddrLine2"]
    if addr != '' and Address["AddrLine3"] != '':
        addr += ', ' + Address["AddrLine3"]
    elif Address["AddrLine3"] != '':
        addr += Address["AddrLine3"]
    if addr != '' and Address["City"] != '':
        addr += ', ' + Address["City"]
    elif Address["City"] != '':
        addr += Address["City"]
    if addr != '' and Address["County"] != '':
        addr += ', ' + Address["County"]
    elif Address["County"] != '':
        addr += Address["County"]
    if addr != '' and Address["StateProvince"] != '':
        addr += ', ' + Address["StateProvince"]
    elif Address["StateProvince"] != '':
        addr += Address["StateProvince"]
    if addr != '' and Address["Country"] != '':
        addr += ', ' + Address["Country"]
    elif Address["Country"] != '':
        addr += Address["Country"]
    if addr != '' and Address["ZipPostalCode"] != '':
        addr += ', ' + Address["ZipPostalCode"]
    elif Address["ZipPostalCode"] != '':
        addr += Address["ZipPostalCode"]

    return addr


def edit_get_source_column_value(edit):
    """
    Gets the current value of the source column of the edited row.
    """
    row = edit.get_edited_row()
    current_value = getattr(row, edit.SourceColumn)
    if edit.SourceColumn in ENUM_FIELDS:
        current_value = current_value.Value if current_value is not None else ''
    return current_value


def edit_get_old_new_value(edit, old_new_field):
    """
    Gets the edit's OldValue or NewValue specified by **old_new_field**.
    **old_new_field** should be the string ``'NewValue'`` or ``'OldValue'``.
    """
    edit_value = getattr(edit, old_new_field)
    if edit.SourceColumn in ENUM_FIELDS:
        edit_value = get_enum_value_row_else_null(edit.SourceColumn, edit_value)
    return edit_value


def apply_edits(ready_edits=None):
    """
    Applies the changes of a list of edits.
    If a list is not provided, it applies all edits whose DateEffective is today.
    For rejected edit additions, this sets the SourceColumn of the edited row to False.
    """
    if ready_edits is None:
        ready_edits = Edit.objects.filter(ReviewStatus='A',
                                          DateEffective__date=datetime.date.today()).exclude(ApprovedBy=None)
    for edit in ready_edits:
        row = edit.get_edited_row()
        edit_value = edit_get_old_new_value(edit, 'NewValue')
        setattr(row, edit.SourceColumn, edit_value)
        row.save()
        edit.IsApplied = True
        edit.save()
        edit_update_old_value_all_awaiting_apply_or_review(edit)
        if edit.SourceTable == "Address":
            """
            Geocode Address objects to set Location fields.
            """
            addr_string = create_addr_string(row)
            if addr_string != '':
                loc = get_elevation(create_addr_string(row))
                location = row.LocationID
                location.Elevation = loc['Elevation']['Value']
                location.Longitude = loc['Longitude']['Value']
                location.Latitude = loc['Latitude']['Value']
                location.save()
    # If an addition edit is rejected, set its status false
    rejected_addition_edits = Edit.objects.filter(ReviewStatus='R',
                                                  EditType='A',
                                                  DateEffective__date=datetime.date.today()).exclude(ApprovedBy=None)
    for edit in rejected_addition_edits:
        row = edit.get_edited_row()
        setattr(row, row.get_relation_status_field(), False)
        row.save()


def revert_edit(user, edit):
    """
    Creates and applies an edit that reverses the change of the given edit.
    The OldValue of the created edit is the current value of the edited field.
    """
    if edit.ReviewStatus == 'P':
        return False
    current_value = edit_get_source_column_value(edit)
    if edit.EditType in {'A', 'D'}:
        next_value = not edit.NewValue
    else:
        next_value = edit.OldValue
    if current_value == next_value:
        return False
    revert_edit_dict = {'User': user,
                        'AHJPK': edit.AHJPK,
                        'SourceTable': edit.SourceTable,
                        'SourceColumn': edit.SourceColumn,
                        'SourceRow': edit.SourceRow,
                        'OldValue': current_value,
                        'NewValue': next_value,
                        'EditType': edit.EditType}
    e = add_edit(revert_edit_dict, ReviewStatus='A', ApprovedBy=user, DateEffective=timezone.now())
    apply_edits(ready_edits=[e])
    return True


def edit_is_resettable(edit):
    """
    Determines if an edit can be reset.

    To be resettable, it must either be:
        - Rejected.
        - Approved, but whose changes have not been applied to the edited row.
        - Approved and applied, but no other edits have been applied after it.
    """
    is_rejected = edit.ReviewStatus == 'R'
    is_approved_not_applied = edit.ReviewStatus == 'A' and not edit.IsApplied
    is_latest_applied = edit.IsApplied and not Edit.objects.filter(SourceTable=edit.SourceTable, SourceRow=edit.SourceRow, SourceColumn=edit.SourceColumn,
                                                                   ReviewStatus='A', IsApplied=True, DateEffective__gt=edit.DateEffective).exists()
    return is_rejected or is_approved_not_applied or is_latest_applied


def edit_make_pending(edit):
    """
    Sets an edit to pending (awaiting approval or rejection).
    """
    edit.ReviewStatus = 'P'
    edit.ApprovedBy = None
    edit.DateEffective = None
    edit.IsApplied = False
    edit.save()


def edit_update_old_value_all_awaiting_apply_or_review(edit):
    """
    Updates the OldValue of all pending or approved but not applied edits
    that modify the same SourceRow and SourceColumn to the SourceColumn's current value.

    :param edit: The reference edit to get the queryset for updating
    """
    current_value = edit_get_source_column_value(edit)
    Edit.objects.filter(SourceTable=edit.SourceTable, SourceRow=edit.SourceRow, SourceColumn=edit.SourceColumn,
                        IsApplied=False, ReviewStatus__in=['A', 'P']).update(OldValue=current_value)


def edit_update_old_value(edit):
    """
    Updates the OldValue of an edit to the current value of
    the SourceColumn of the edited row.
    """
    edit.OldValue = edit_get_source_column_value(edit)
    edit.save()


def edit_undo_apply(edit):
    """
    Sets the SourceColumn of the edited row to
    the OldValue of the edit.
    """
    row = edit.get_edited_row()
    old_value = edit_get_old_new_value(edit, 'OldValue')
    setattr(row, edit.SourceColumn, old_value)
    row.save()


def edit_is_rejected_addition(edit):
    """
    Returns boolean whether an edit is a rejected addition.
    """
    return edit.EditType == 'A' and edit.ReviewStatus == 'R'


def reset_edit(user, edit, force_resettable=False, skip_undo=False):
    """
    When an edit is reset, it is set to a pending state, and is again awaiting
    approval or rejection.

    .. note::

        If an edit was applied, its change must be undone. In addition, rejected edit
        additions set their SourceColumn False, so that must also be undone (see apply_edits).

    If an edit is not resettable, it is instead reverted.
    """
    if edit_is_resettable(edit) or force_resettable:
        if (edit.IsApplied or edit_is_rejected_addition(edit)) and not skip_undo:
            """
            If an edit was applied, its change must be undone. In addition, rejected edit
            additions set their SourceColumn False, so that must also be undone (see apply_edits).
            """
            edit_undo_apply(edit)
        else:
            edit_update_old_value(edit)
        edit_make_pending(edit)
        return True
    return False


####################


@api_view(['POST'])
@authentication_classes([WebpageTokenAuth])
@permission_classes([IsAuthenticated])
def edit_review(request):
    """
    Sets an edit's ReviewStatus to 'A' for approval or 'R' for rejection,
    and sets the DateEffective.
    """
    try:
        eid = request.data['EditID']  # required
        stat = request.data['Status']  # required
        if stat != 'A' and stat != 'R':
            raise ValueError('Invalid edit status ' + str(status))
        user = request.user
        edit = Edit.objects.get(EditID=eid)
        if not user.is_superuser and not AHJUserMaintains.objects.filter(UserID=user,
                                                                         AHJPK=edit.AHJPK,
                                                                         MaintainerStatus=True).exists():
            return Response('You do not have permission to perform this action', status=status.HTTP_403_FORBIDDEN)
        edit.ReviewStatus = stat
        edit.ApprovedBy = request.user
        tomorrow = timezone.now() + datetime.timedelta(days=1)
        if not edit.DateEffective or edit.DateEffective < tomorrow:
            edit.DateEffective = tomorrow
        edit.save()  # commit changes
        return Response('Success!', status=status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


def create_row(model, obj):
    """
    Adds a row to the table represented by the model using the values in **obj**.
    **obj** is allowed to have key-value pairs whose value is a nested dict,
    and key is another model name. Rows using these nested dict values will also
    be created for the model name key.

    :param model: Model whose table a row is added to
    :param obj: The dict containing the values to instantiate the row with
    :return: the row instance created
    """
    field_dict = {}
    rel_one_to_one = []
    rel_many_to_many = []
    for field, value in obj.items():
        if value == '':
            continue
        elif type(value) is dict:
            """
            NOTE: This assumes the field name matches the name of its model!
            For example, a serialized 'Contact' has the field 'Address', and Address is a model
            """
            if field == "Address":
                """
                Geocode Address objects to set Location fields.
                """
                addr = get_elevation(addr_string_from_dict(value))
                value["Location"]["Longitude"] = addr["Longitude"]["Value"]
                value["Location"]["Latitude"] = addr["Latitude"]["Value"]
                value["Location"]["Elevation"] = addr["Elevation"]["Value"]
            rel_one_to_one.append(create_row(apps.get_model('ahj_app', field), value))
        elif type(value) is list:
            plurals_to_singular = {'Contacts': 'Contact'}
            if field in plurals_to_singular:
                field = plurals_to_singular[field]
            for v in value:
                rel_many_to_many.append(create_row(apps.get_model('ahj_app', field), v))
        else:
            field_dict[field] = get_enum_value_row(field, value) if field in ENUM_FIELDS else value

    model_fields = model._meta.fields

    # Establish all one-to-one relations with row
    for r in rel_one_to_one:
        found_field = False
        for field in model_fields:
            if getattr(field, 'remote_field') is not None and field.remote_field.model.__name__ == r.__class__.__name__:
                found_field = True
                field_dict[field.name] = r
        if not found_field:
            raise ValueError('Model \'{parent_model}\' has no one-to-one relation with \'{rel_model}\''.format(parent_model=model.__name__, rel_model=r.__class__.__name__))

    if model.__name__ == 'PermitIssueMethod' or model.__name__ == 'DocumentSubmissionMethod':
        row = model.objects.get(**field_dict)
    else:
        row = model.objects.create(**field_dict)

    # Establish all many-to-many relations with row
    for r in rel_many_to_many:
        rel = r.create_relation_to(row)
        setattr(rel, r.get_relation_status_field(), True)
        rel.save()

    return row


def get_serializer(row):
    """
    Returns the serializer class for a given row object instance.

    :param row: Instance of a table representing an object on the AHJ object
    :return: A serializer class for **row**
    """
    serializers = {
        'AHJ': AHJSerializer,
        'AHJInspection': AHJInspectionSerializer,
        'Contact': ContactSerializer,
        'DocumentSubmissionMethod': DocumentSubmissionMethodUseSerializer,
        'AHJDocumentSubmissionMethodUse': DocumentSubmissionMethodUseSerializer,
        'EngineeringReviewRequirement': EngineeringReviewRequirementSerializer,
        'FeeStructure': FeeStructureSerializer,
        'PermitIssueMethod': PermitIssueMethodUseSerializer,
        'AHJPermitIssueMethodUse': PermitIssueMethodUseSerializer
    }
    return serializers[row.__class__.__name__]


@api_view(['POST'])
@authentication_classes([WebpageTokenAuth])
@permission_classes([IsAuthenticated])
def edit_addition(request):
    """
    Endpoint for submitting edits to add objects on an AHJ.
    It expects request.data to be a dict of the form:

    .. code-block:: python

        {
            'AHJPK': <AHJPK_of_AHJ_edited>,  # i.e. 123
            'SourceTable': <table_of_object_added>,  # i.e. 'Contact'
            'ParentTable': <table_of_object_related_to_SourceTable>,  # i.e. 'AHJ' or 'AHJInspection'
            'ParentID': <row_of_object_related_to_SourceTable>,  # i.e. 123
            'Value': [
                <dict_of_objects_to_add>
            ]
        }

    The <dict_of_objects_to_add> is a dict with a subset of the entries in the dicts produced
    from the SourceTable objects by serializers.py. Note that if the dict produced by
    serializers.py includes a nested dict entry, that entry type must be included even if
    its an empty dict value. Here are examples:

    .. code-block:: python

        # Contact
        {
            '<contact_field>': <value>,
            ...,
            'Address': <address_dict>
            \"\"\"
            This 'Address' entry is required since it is a nested dict, even if <address_dict> is emtpy ({}).
            Note <address_dict> also has a 'Location' nested dict entry that is also required.
            \"\"\"
        }

        # AHJInspection
        {
            '<ahj_inspection_field>': <value>,
            ...,
            'Contacts': [  # This is not required since it is a nested array
                <contact_dict>,
                ...,
            ]
        }

        # DocumentSubmissionMethod and PermitIssueMethod
        {
            'Value': <dsm/pim_method>
        }
    """
    try:
        source_table = request.data.get('SourceTable')
        response_data, response_status = [], status.HTTP_200_OK
        with transaction.atomic():
            model = apps.get_model('ahj_app', source_table)
            parent_table = request.data.get('ParentTable')
            parent_id = request.data.get('ParentID')
            parent_model = apps.get_model('ahj_app', parent_table)
            parent_row = parent_model.objects.get(pk=parent_id)
            ahjpk = request.data.get('AHJPK')
            ahj = AHJ.objects.get(AHJPK=ahjpk)
            new_objs = request.data.get('Value', [])

            """
            Boolean for if the addition is a one-to-many relation to AHJ.
            For example, Contact, FeeStructure and EngineeringReviewRequirement
            """
            AHJ_one_to_many = 'AHJPK' in [field.name for field in model._meta.fields]
            edits = []
            for obj in new_objs:
                if AHJ_one_to_many:
                    obj['AHJPK'] = ahj

                row = create_row(model, obj)
                edit_info_row = row.create_relation_to(parent_row)
                e = { 'User'         : request.user,
                      'AHJPK'        : ahj,
                      'SourceTable'  : edit_info_row.__class__.__name__,
                      'SourceColumn' : row.get_relation_status_field(),
                      'SourceRow'    : edit_info_row.pk,
                      'OldValue'     : None,
                      'NewValue'     : True,
                      'EditType'     : 'A' }
                edit = add_edit(e)
                edits.append(edit)

                response_data.append(get_serializer(row)(edit_info_row).data)
        return Response(response_data, status=response_status)
    except Exception as e:
        print('ERROR in edit_addition', str(e))
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([WebpageTokenAuth])
@permission_classes([IsAuthenticated])
def edit_deletion(request):
    """
    Endpoint for submitting edits to delete objects on an AHJ.
    It expects request.data to be a dict of the form:

    .. code-block:: python

        {
            'AHJPK': <AHJPK_of_AHJ_edited>,  # i.e. 123
            'SourceTable': <table_of_object_deleted>,  # i.e. 'Contact'
            'Value': [
                <source_table_row_primary_key>,  # i.e. 123
                ...
            ]
        }
    """
    try:
        source_table = request.data.get('SourceTable')
        response_data, response_status = [], status.HTTP_200_OK
        with transaction.atomic():
            model = apps.get_model('ahj_app', source_table)
            ahjpk = request.data.get('AHJPK')
            ahj = AHJ.objects.get(AHJPK=ahjpk)
            pks_to_delete = request.data.get('Value', [])

            for pk in pks_to_delete:
                row = model.objects.get(pk=pk)
                e = { 'User'         : request.user,
                      'AHJPK'        : ahj,
                      'SourceTable'  : source_table,
                      'SourceColumn' : row.get_relation_status_field(),
                      'SourceRow'    : row.pk,
                      'OldValue'     : True,
                      'NewValue'     : False,
                      'EditType'     : 'D' }
                edit = add_edit(e)

                response_data.append(get_serializer(row)(row).data)
        return Response(response_data, status=response_status)
    except Exception as e:
        print('ERROR in edit_deletion', str(e))
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([WebpageTokenAuth])
@permission_classes([IsAuthenticated])
def edit_update(request):
    """
    Endpoint for submitting edits to update fields on an AHJ.
    It expects request.data to be an array of dicts of the form:

    .. code-block:: python

        [
            {
                'AHJPK': <AHJPK_of_AHJ_edited>,  # i.e. 123
                'SourceTable': <table_of_object_of_AHJ_edited>,  # i.e. 'Contact'
                'SourceRow': <row_edited>,  # i.e. 123
                'SourceColumn': <column_edited>,  # i.e. 'Email'
                'NewValue': <new_value_for_row_column>,  # i.e. 'official@ahj.gov'
            }
        ]
    """
    try:
        response_data, response_status = [], status.HTTP_200_OK
        with transaction.atomic():
            es = request.data
            edits = []
            for e in es:
                e['AHJPK'] = AHJ.objects.get(AHJPK=e['AHJPK'])
                model = apps.get_model('ahj_app', e['SourceTable'])
                row = model.objects.get(pk=e['SourceRow'])
                old_value = getattr(row, e['SourceColumn'])
                if e['SourceColumn'] in ENUM_FIELDS:
                    old_value = old_value.Value if old_value is not None else ''
                e['OldValue'] = old_value
                e['User'] = request.user
                e['EditType'] = 'U'
                edit = add_edit(e)
                edits.append(edit)
                response_data.append(EditSerializer(edit).data)
        return Response(response_data, status=response_status)
    except Exception as e:
        print('ERROR in edit_update', str(e))
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def edit_list(request):
    """
    Endpoint returning all edits made to an AHJ.
    This expects an ``AHJPK`` in the query parameters.
    """
    try:
        edits = Edit.objects.filter(AHJPK=request.query_params.get('AHJPK'))
        return Response(EditSerializer(edits, many=True, context={'drop_users': True}).data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user_edits(request):
    """
    Endpoint returning all edits made a user specified by UserID.
    Only the Usernames of the ``ChangedBy`` and ``ApprovedBy`` users are serialized.
    This expects a ``UserID`` in the query parameters.
    """
    try:
        edits = Edit.objects.filter(ChangedBy=request.query_params.get('UserID'))
        return Response(EditSerializer(edits, many=True, context={'drop_users': True}).data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
