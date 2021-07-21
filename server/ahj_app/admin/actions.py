import csv
import datetime

from django.core.checks import messages
from django.forms import formset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.utils import timezone

from .form import UserResetPasswordForm, UserDeleteToggleAPITokenForm, EditApproveForm, UserGenerateAPITokenForm
from ..models import User, APIToken, Edit, AHJUserMaintains, Comment
from ..usf import dict_filter_keys_start_with, ENUM_FIELDS
from ..views_edits import apply_edits, reset_edit, edit_is_resettable


def get_value_or_primary_key(obj, field):
    """
    Retrieves the value of a field from an object.
    If the value is None, empty string is returned.
    If the field is an enum field, its value is returned.
    If the field is a related field, the its primary key is returned.
    """
    value = getattr(obj, field)
    field_class_name = obj._meta.get_field(field).__class__.__name__
    if value is None:
        value = ''
    elif field in ENUM_FIELDS:
        value = value.Value
    elif field_class_name == 'ForeignKey' or field_class_name == 'OneToOneField':
        value = value.pk
    return value


class ExportCSVMixin:
    """
    Mixin to for an admin model to inherit to add an export_csv admin action.
    """
    def export_csv(self, request, queryset):
        """
        Returns a CSV file exporting all the rows in the queryset.
        """
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={timezone.now()}_{self.model.__name__}_table.csv'
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([get_value_or_primary_key(obj, field) for field in field_names])
        return response

    export_csv.short_description = 'Export CSV'


def reset_password(user, raw_password):
    """
    Sets and saves a user's password.
    """
    user.set_password(raw_password)
    user.save()


def user_reset_password(self, request, queryset):
    """
    Admin action for the User model. The admin can set a new password
    for one user. The new password is hashed, and then saved.
    """
    if 'apply' in request.POST:
        """
        The form has been filled out and submitted.
        """
        password = request.POST['password']
        user_id = request.POST['_selected_action']
        user = User.objects.get(UserID=user_id)
        reset_password(user, password)
        self.message_user(request, 'Success', level=messages.INFO)
        return HttpResponseRedirect(request.get_full_path())
    if queryset.count() > 1:
        """
        Only support setting the password for one user at a time.
        """
        self.message_user(request, 'Please select one user when running this action.', level=messages.ERROR)
        return HttpResponseRedirect(request.get_full_path())
    form = UserResetPasswordForm()
    return render(request, 'admin/user_reset_password.html', context={
        'request': request,
        'user': queryset.first(),
        'form': form
    })


user_reset_password.short_description = 'Reset password'


def partition_by_field(queryset, field, value):
    """
    Returns two querysets from the queryset:
     - queryset of rows whose field value matches the value
     - queryset of rows whose field value does not match the value
    """
    with_field_value = queryset.filter(**{field: value})
    without_field_value = queryset.exclude(**{field: value})
    return with_field_value, without_field_value


def set_date_from_str(date_str):
    """
    Returns a date object from a string formatted in '%Y-%m-%d'.
    """
    try:
        return timezone.make_aware(datetime.datetime.strptime(date_str, '%Y-%m-%d'))
    except ValueError:
        return None


def process_generate_api_token_data(post_data):
    """
    This expects the post_data to contain an array called 'user_to_form'.
    Each item in this array is of the form:
     - '<UserID>.<form_prefix>' (i.e. '1.form-0')
    Each form then may add two form data key-value pairs:
     - '<form_prefix>-expiration_date': '<date>' (i.e. 'form-0-expiration_date': '2021-06-04')
    """
    user_to_form_pairs = [pair.split('.') for pair in post_data.getlist('user_to_form')]
    user_form_data = []
    for user_id, form_prefix in user_to_form_pairs:
        user = User.objects.get(UserID=user_id)
        form_data = dict_filter_keys_start_with(form_prefix, post_data)
        date_str = '-'.join([form_data.get('ExpirationDate_year', ''),
                             form_data.get('ExpirationDate_month', ''),
                             form_data.get('ExpirationDate_day', '')])
        expiration_date = set_date_from_str(date_str=date_str)
        user_form_data.append({'user': user,
                               'expires': expiration_date})
    return user_form_data


def user_generate_api_token(self, request, queryset):
    """
    Admin action for the User model. The admin can select one or
    more users and generate an API token for them. If selected users
    already have an API token, a new API will not be generated for them.
    """
    if 'apply' in request.POST:
        """
        The form has been filled out and submitted.
        """
        action_data = process_generate_api_token_data(request.POST)
        for item in action_data:
            APIToken.objects.create(user=item['user'], expires=item['expires'])
        self.message_user(request, 'Success', level=messages.INFO)
        return HttpResponseRedirect(request.get_full_path())
    users_without_tokens, users_with_tokens = partition_by_field(queryset, 'api_token', None)
    users_with_tokens = users_with_tokens.order_by('Email')
    users_without_tokens = users_without_tokens.order_by('Email')
    formset = formset_factory(UserGenerateAPITokenForm, extra=queryset.count())()
    return render(request, 'admin/user_generate_api_token.html', context={
        'request': request,
        'users_without_tokens': users_without_tokens,
        'users_without_tokens_and_forms': zip(users_without_tokens, formset),
        'user_token_tuples': zip(users_with_tokens, users_with_tokens.values_list('api_token', flat=True))
    })


user_generate_api_token.short_description = 'Generate API token'


def delete_toggle_api_token(user, toggle=None, delete=False):
    """
    Modifies a user's API token by either deleting it or toggling it on/off.
    """
    if not hasattr(user, 'api_token'):
        return
    if delete:
        user.api_token.delete()
        return
    if toggle is not None:
        user.api_token.is_active = toggle
        user.api_token.save()


def set_toggle(form_value):
    """
    Used with an HTML dropdown input with values:
    'On', 'Off','DoNothing'
    """
    if form_value == 'On':
        return True
    elif form_value == 'Off':
        return False
    else:
        return None


def set_delete(form_value):
    """
    Return True if form_value is 'on'.
    Used with an HTML checkbox input.
    """
    if form_value == 'on':
        return True
    return False


def process_delete_toggle_api_token_data(post_data):
    """
    This expects the post_data to contain an array called 'user_to_form'.
    Each item in this array is of the form:
     - '<UserID>.<form_prefix>' (i.e. '1.form-0')
    Each form then may add two form data key-value pairs:
     - '<form_prefix>-toggle': '<On,Off,DoNothing>' (i.e. 'form-0-toggle': 'On')
     - '<form_prefix>-delete_token': 'on' (i.e. 'form-0-delete_token': 'on')
    """
    user_to_form_pairs = [pair.split('.') for pair in post_data.getlist('user_to_form')]
    user_form_data = []
    for user_id, form_prefix in user_to_form_pairs:
        user = User.objects.get(UserID=user_id)
        form_data = dict_filter_keys_start_with(form_prefix, post_data)
        toggle_api_token = form_data.get('toggle', '')
        delete_api_token = form_data.get('delete_token', '')
        user_form_data.append({'user': user,
                               'toggle': set_toggle(toggle_api_token),
                               'delete': set_delete(delete_api_token)})
    return user_form_data


def user_delete_toggle_api_token(self, request, queryset):
    """
    Admin action for the User model. The admin can select one or
    more users and delete or toggle on/off each user's API token.
    If selected users do not have an API token, there will be no
    options displayed for them.
    """
    if 'apply' in request.POST:
        """
        The form has been filled out and submitted.
        """
        action_data = process_delete_toggle_api_token_data(request.POST)
        for item in action_data:
            delete_toggle_api_token(user=item['user'], toggle=item['toggle'], delete=item['delete'])
        self.message_user(request, 'Success', level=messages.INFO)
        return HttpResponseRedirect(request.get_full_path())
    users_without_tokens, users_with_tokens = partition_by_field(queryset, 'api_token', None)
    users_with_tokens = users_with_tokens.order_by('Email')
    users_without_tokens = users_without_tokens.order_by('Email')
    formset = formset_factory(UserDeleteToggleAPITokenForm, extra=queryset.count())()
    return render(request, 'admin/user_delete_toggle_api_token.html', context={
        'request': request,
        'users_without_tokens': users_without_tokens,
        'users_and_forms': zip(users_with_tokens, formset),
        'users_with_tokens': users_with_tokens
    })


user_delete_toggle_api_token.short_description = 'Delete/Toggle API Token'


def build_url_parameters_for_change_list_filtering(queryset, field_key_pairs):
    """
    Builds a URL query of key-value pairs for each field of the form:
     - <field>=<value>,...<value>
    """
    query = '?'
    for f in field_key_pairs:
        values = [str(v) for v in queryset.values_list(f['field'], flat=True)]
        query += f'{f["key"]}={",".join(values)}&'
    return query


def field_key_pair(field, key):
    return {'field': field, 'key': key}


def load_change_list_with_queryset(request, queryset, model_name, field_key_pairs):
    """
    Creates the redirect response to a change list with a url query created from
    the queryset and field_key_pairs.
    """
    query = build_url_parameters_for_change_list_filtering(queryset, field_key_pairs)
    return HttpResponseRedirect(f'{request.build_absolute_uri(f"/admin/ahj_app/{model_name}/")}{query}')


def user_query_api_tokens(self, request, queryset):
    """
    Admin action for the User model. Redirects the admin to
    a change list of the selected users' APITokens.
    Users without APITokens are filtered from the selection.
    """
    model_name = 'apitoken'
    field_key_pairs = [field_key_pair('api_token__user', 'user')]
    queryset = queryset.exclude(api_token=None)
    return load_change_list_with_queryset(request, queryset, model_name, field_key_pairs)


user_query_api_tokens.short_description = 'Query API Tokens'


def user_query_ahjs_is_ahj_official_of(self, request, queryset):
    """
    Admin action for the User model. Redirects the admin to
    a change list of AHJs the selected users are AHJ officials of.
    """
    model_name = 'ahj'
    field_key_pairs = [field_key_pair('AHJPK', 'AHJPK')]
    queryset = AHJUserMaintains.objects.filter(UserID__in=queryset, MaintainerStatus=True)
    return load_change_list_with_queryset(request, queryset, model_name, field_key_pairs)


user_query_ahjs_is_ahj_official_of.short_description = 'Query Is AHJ Official Of'


def user_query_submitted_edits(self, request, queryset):
    """
    Admin action for the User model. Redirects the admin to
    a change list of edits submitted by the selected users.
    """
    model_name = 'edit'
    field_key_pairs = [field_key_pair('ChangedBy', 'ChangedBy')]
    queryset = Edit.objects.filter(ChangedBy__in=queryset)
    return load_change_list_with_queryset(request, queryset, model_name, field_key_pairs)


user_query_submitted_edits.short_description = 'Query Submitted Edits'


def user_query_approved_edits(self, request, queryset):
    """
    Admin action for the User model. Redirects the admin to
    a change list of edits approved by the selected users.
    """
    model_name = 'edit'
    field_key_pairs = [field_key_pair('ApprovedBy', 'ApprovedBy')]
    queryset = Edit.objects.filter(ApprovedBy__in=queryset)
    return load_change_list_with_queryset(request, queryset, model_name, field_key_pairs)


user_query_approved_edits.short_description = 'Query Approved Edits'


def user_query_submitted_comments(self, request, queryset):
    """
    Admin action for the User model. Redirects the admin to
    a change list of comments submitted by the selected users.
    """
    model_name = 'comment'
    field_key_pairs = [field_key_pair('UserID', 'UserID')]
    queryset = Comment.objects.filter(UserID__in=queryset)
    return load_change_list_with_queryset(request, queryset, model_name, field_key_pairs)


user_query_submitted_comments.short_description = 'Query Submitted Comments'


def process_approve_edits_data(post_data, requesting_user):
    """
    This expects the post_data to contain an array called 'edit_to_form'.
    Each item in this array is of the form:
     - '<EditID>.<form_prefix>' (i.e. '1.form-0')
    Each form then may add two form data key-value pairs:
     - '<form_prefix>-date_effective': '<date>' (i.e. 'form-0-date_effective': '2021-06-04')
    """
    edit_to_form_pairs = [pair.split('.') for pair in post_data.getlist('edit_to_form')]
    edit_form_data = []
    for edit_id, form_prefix in edit_to_form_pairs:
        edit = Edit.objects.get(EditID=edit_id)
        form_data = dict_filter_keys_start_with(form_prefix, post_data)
        date_str = '-'.join([form_data.get('DateEffective_year', ''),
                             form_data.get('DateEffective_month', ''),
                             form_data.get('DateEffective_day', '')])
        date_effective = set_date_from_str(date_str=date_str)
        if date_effective is None:
            continue
        apply_now = date_effective.date() <= datetime.date.today()
        if apply_now:
            date_effective = timezone.now()
        edit_form_data.append({'edit': edit,
                               'approved_by': requesting_user,
                               'date_effective': date_effective,
                               'apply_now': apply_now})
    return edit_form_data


def approve_edit(edit, approved_by, date_effective, apply_now):
    """
    Sets the fields necessary to approve and apply an edit.
    If apply_now is True, then the edit will be applied immediately.
    """
    edit.ApprovedBy = approved_by
    edit.DateEffective = date_effective
    edit.ReviewStatus = 'A'
    edit.save()
    if apply_now:
        apply_edits(ready_edits=[edit])


def edit_approve_edits(self, request, queryset):
    """
    Admin action for the Edit model. The admin can select one or
    more edits and approve each one by setting its date effective and approving user.
    """
    queryset = queryset.order_by('DateRequested')
    if 'apply' in request.POST:
        """
        The form has been filled out and submitted.
        """
        action_data = process_approve_edits_data(request.POST, request.user)
        for item in action_data:
            approve_edit(edit=item['edit'],
                         approved_by=item['approved_by'],
                         date_effective=item['date_effective'],
                         apply_now=item['apply_now'])
        self.message_user(request, 'Success', level=messages.INFO)
        return HttpResponseRedirect(request.get_full_path())
    formset = formset_factory(EditApproveForm, extra=queryset.count())()
    return render(request, 'admin/edit_approve_edits.html', context={
        'request': request,
        'edits_and_forms': zip(queryset, formset),
        'edits': queryset
    })


edit_approve_edits.short_description = 'Approve Edits'


def edit_roll_back_edits(self, request, queryset):
    """
    Admin action for the Edit model. The admin can select one or
    more edits and each one will be rolled back. To roll back an edit,
    it is either reset (it is changed to a pending edit, and its
    changes are undone), or reverted (a new edit is created that
    reverses the change made by the selected edit).
    """
    queryset = queryset.order_by('-DateEffective')
    pending_edits, non_pending_edits = partition_by_field(queryset, 'ReviewStatus', 'P')
    resettable_edits = [edit for edit in non_pending_edits if edit_is_resettable(edit)]
    non_resettable_edits = [edit for edit in non_pending_edits if not edit_is_resettable(edit)]
    if 'apply' in request.POST:
        """
        The form has been filled out and submitted.
        """
        for edit in non_resettable_edits:
            reset_edit(request.user, edit)
        for edit in resettable_edits:
            revert_occurred = not edit_is_resettable(edit)
            reset_edit(request.user, edit, force_resettable=revert_occurred, skip_undo=revert_occurred)
        self.message_user(request, 'Success', level=messages.INFO)
        return HttpResponseRedirect(request.get_full_path())
    return render(request, 'admin/edit_roll_back_edits.html', context={
        'request': request,
        'pending_edits': pending_edits,
        'resettable_edits': resettable_edits,
        'non_resettable_edits': non_resettable_edits
    })


edit_roll_back_edits.short_description = 'Roll back Edits'


def edit_query_submitting_users(self, request, queryset):
    """
    Admin action for the Edit model. Redirects the admin to
    a change list of users who submitted the selected edits.
    """
    model_name = 'user'
    field_key_pairs = [field_key_pair('UserID', 'UserID')]
    queryset = User.objects.filter(UserID__in=queryset.values_list('ChangedBy', flat=True))
    return load_change_list_with_queryset(request, queryset, model_name, field_key_pairs)


edit_query_submitting_users.short_description = 'Query Submitting Users'


def edit_query_approving_users(self, request, queryset):
    """
    Admin action for the Edit model. Redirects the admin to
    a change list of users who approved the selected edits.
    """
    model_name = 'user'
    field_key_pairs = [field_key_pair('UserID', 'UserID')]
    queryset = User.objects.filter(UserID__in=queryset.values_list('ApprovedBy', flat=True))
    return load_change_list_with_queryset(request, queryset, model_name, field_key_pairs)


edit_query_approving_users.short_description = 'Query Approving Users'


def ahj_query_ahj_official_users(self, request, queryset):
    """
    Admin action for the AHJ model. Redirects the admin to
    a change list of users who are AHJ officials of the selected AHJs.
    """
    model_name = 'user'
    field_key_pairs = [field_key_pair('UserID', 'UserID')]
    queryset = AHJUserMaintains.objects.filter(AHJPK__in=queryset, MaintainerStatus=True)
    return load_change_list_with_queryset(request, queryset, model_name, field_key_pairs)


ahj_query_ahj_official_users.short_description = 'Query AHJ Official Users'


def comment_query_submitting_users(self, request, queryset):
    """
    Admin action for the Comment model. Redirects the admin to
    a change list of users who submitted the selected comments.
    """
    model_name = 'user'
    field_key_pairs = [field_key_pair('UserID', 'UserID')]
    queryset = User.objects.filter(UserID__in=queryset.values_list('UserID', flat=True))
    return load_change_list_with_queryset(request, queryset, model_name, field_key_pairs)


comment_query_submitting_users.short_description = 'Query Submitting Users'
