from operator import attrgetter

from django.apps import apps
from django.contrib import admin
from django.contrib.gis import admin as geo_admin
from simple_history.admin import SimpleHistoryAdmin

from .actions import user_reset_password, user_generate_api_token, user_delete_toggle_api_token, edit_approve_edits, \
    edit_roll_back_edits, ExportCSVMixin, user_query_api_tokens, user_query_ahjs_is_ahj_official_of, \
    user_query_submitted_edits, user_query_approved_edits, edit_query_submitting_users, edit_query_approving_users, \
    comment_query_submitting_users, user_query_submitted_comments, ahj_query_ahj_official_users
from .form import UserChangeForm

USER_DATA_MODELS = {
    'APIToken',
    'Comment',
    'Edit',
    'User',
}

POLYGON_DATA_MODELS = {
    'Polygon',
    'StatePolygon',
    'CountyPolygon',
    'CityPolygon',
    'CountySubdivisionPolygon',
    'StateTemp',
    'CountyTemp',
    'CityTemp',
    'CousubTemp'
}


class AHJRegistryAdminSite(admin.AdminSite):
    """
    Custom admin site for the AHJ Registry. Changes include:
    site_header, site_title, index_title, categorized models.
    """
    site_header = 'AHJ Registry Admin Dashboard'
    site_title = 'AHJ Registry Admin Dashboard'
    index_title = 'AHJ Registry Admin Dashboard'

    def get_custom_app_dict(self, name, app_label, app_url, has_module_perms, models):
        """
        Helper to categorize models under a fake application label.
        """
        return {
            'name': name,
            'app_label': app_label,
            'app_url': app_url,
            'has_module_perms': has_module_perms,
            'models': models
        }

    def get_app_list(self, request):
        """
        Creates a list of dict to tell the admin site index page
        how to group the models of the installed apps. This was overridden
        to create custom groupings for the models of the ahj_app.
        """
        app_list = super().get_app_list(request)
        ahj_app = [app for app in app_list if app['app_label'] == 'ahj_app']
        if len(ahj_app) == 0:
            """
            Sometimes the super class' get_app_list returns an empty list.
            """
            return app_list
        ahj_app = ahj_app[0]

        """
        Puts the ahj_app models into these categories: User Data, AHJ Data, Polygon Data.
        """
        user_data_models = [model for model in ahj_app['models'] if model['object_name'] in USER_DATA_MODELS]
        ahj_data_models = [model for model in ahj_app['models'] if model['object_name'] not in USER_DATA_MODELS.union(POLYGON_DATA_MODELS) and not model['object_name'].startswith('Historical')]
        polygon_data_models = [model for model in ahj_app['models'] if model['object_name'] in POLYGON_DATA_MODELS]
        new_app_list = []
        new_app_list.append(self.get_custom_app_dict('User Data', 'user_data', ahj_app['app_url'], ahj_app['has_module_perms'], user_data_models))
        new_app_list.append(self.get_custom_app_dict('AHJ Data', 'ahj_data', ahj_app['app_url'], ahj_app['has_module_perms'], ahj_data_models))
        new_app_list.append(self.get_custom_app_dict('Polygon Data', 'polygon_data', ahj_app['app_url'], ahj_app['has_module_perms'], polygon_data_models))
        return new_app_list


"""
Tell Django to use our custom admin site.
"""
admin.site = AHJRegistryAdminSite()


def is_char_field(model_field):
    """
    Checks if a model field is a char field.
    """
    class_name = model_field.__class__.__name__
    return class_name == 'CharField'


def is_related_field(model_field):
    """
    Checks if a model field is a related field.
    """
    class_name = model_field.__class__.__name__
    return class_name == 'ForeignKey' or class_name == 'OneToOneField'


def get_queryset(self, request):
    """
    Overridden to filter queryset by customized url query parameters.
    These parameter key-value pairs are of the form:
    - <field>=<value>,...<value>
    The GET data before calling super().get_queryset so
    that the queryset it returns is not filtered.
    """
    field_names = {field.name for field in self.model._meta.fields}
    query_dict = {}
    request.GET = request.GET.copy()
    for k in request.GET.keys():
        if k in field_names:
            query_dict[f'{k}__in'] = [v for v in request.GET.get(k).split(',') if v != '']
    for k in query_dict.keys():
        field = k[:k.index('_')]
        if field in request.GET.keys():
            request.GET.pop(field)
    qs = super(self.__class__, self).get_queryset(request)
    if len(query_dict) != 0:
        qs = qs.filter(**query_dict)
    return qs


def get_default_model_admin_class(model, geo=False):
    """
    For a given model, returns a default admin model with:
    - A search bar that searches all CharField fields of the model.
    - A table to display the primary key and all CharField fields of the model.
    - Turned-off dropdown selection of related models in the model detail view.
    - CSV export admin action
    - Customized get_queryset method to support multiple values to URL parameter keys.
    If geo=True, then creates a OSMGeoAdmin for a nicer view of the GIS features.
    """
    model_fields = [field for field in model._meta.fields]
    if geo:
        class DefaultPolygonAdmin(geo_admin.OSMGeoAdmin, ExportCSVMixin, SimpleHistoryAdmin):
            list_display = [field.name for field in model_fields if not is_related_field(field)]
            history_list_display = ["status"]
            search_fields = list_display
            raw_id_fields = [field.name for field in model_fields if is_related_field(field)]
            actions = ['export_csv']
            get_queryset = get_queryset
        return DefaultPolygonAdmin
    else:
        class DefaultAdmin(SimpleHistoryAdmin, ExportCSVMixin):
            list_display = [field.name for field in model_fields if not is_related_field(field)]
            history_list_display = ["status"]
            search_fields = list_display
            raw_id_fields = [field.name for field in model_fields if is_related_field(field)]
            actions = ['export_csv']
            get_queryset = get_queryset
        return DefaultAdmin


def create_admin_get_attr_function(name, dotted_path, admin_order_field, short_description):
    """
    Returns a function to be added to a class definition (an admin model) that takes
    an object and returns an attribute value (possibly nested). If the attribute is
    callable, it returns the value the callable attribute returns.
    """
    def temp_func(self, obj):
        value = attrgetter(dotted_path)(obj)
        if callable(value):
            return value()
        return value
    temp_func.__name__ = name
    temp_func.admin_order_field = admin_order_field
    temp_func.short_description = short_description
    return temp_func


def get_attr_info_dict(name, dotted_path, admin_order_field, short_description):
    """
    Returns a dict with keys named, dotted_path, admin_order_field, and short_description.
    """
    return {
        'name': name,
        'dotted_path': dotted_path,
        'admin_order_field': admin_order_field,
        'short_description': short_description
    }


def get_action_info_dict(name, function):
    """
    Returns a dict with keys name and function.
    """
    return {
        'name': name,
        'function': function
    }


"""
Create default admin models for each model in ahj_app.
"""
model_admin_dict = {}
for model in apps.all_models['ahj_app'].values():
    if 'Polygon' in model.__name__:
        admin_model = get_default_model_admin_class(model, geo=True)
    else:
        admin_model = get_default_model_admin_class(model)
    model_admin_dict[model.__name__] = {
        'model': model,
        'admin_model': admin_model
    }


"""
Customizing APIToken Admin Model:
Added to list_display:
 - The user's email.
 - The user's company affiliation.
 - If the user is an AHJ Official of any AHJ.
"""
api_token_admin_model = model_admin_dict['APIToken']['admin_model']
admin_attrs_to_add = []
admin_attrs_to_add.append(get_attr_info_dict('get_user_email', 'user.Email', 'email', 'Email'))
admin_attrs_to_add.append(get_attr_info_dict('get_user_company_affiliation', 'user.CompanyAffiliation', 'company_affiliation', 'Company Affiliation'))
admin_attrs_to_add.append(get_attr_info_dict('get_user_is_ahj_official', 'user.is_ahj_official', 'ahj_official', 'Is AHJ Official'))
for attr in admin_attrs_to_add:
    setattr(api_token_admin_model, attr['name'],
            create_admin_get_attr_function(attr['name'], attr['dotted_path'], attr['admin_order_field'], attr['short_description']))
    api_token_admin_model.list_display.append(attr['name'])


"""
Customizing User Admin Model:
Adding Admin Actions:
 - Reset Password.
 - Generate API Token.
 - Delete/Toggle API Token.
 - Query API Tokens
 - Query Is AHJ Official Of
 - Query Submitted Edits
 - Query Approved Edits
 - Query Submitted Comments
Removing from list_display:
 - The user's hashed password.
"""
user_admin_model = model_admin_dict['User']['admin_model']
admin_actions_to_add = []
admin_actions_to_add.append(get_action_info_dict('user_reset_password', user_reset_password))
admin_actions_to_add.append(get_action_info_dict('user_generate_api_token', user_generate_api_token))
admin_actions_to_add.append(get_action_info_dict('user_delete_toggle_api_token', user_delete_toggle_api_token))
admin_actions_to_add.append(get_action_info_dict('user_query_api_tokens', user_query_api_tokens))
admin_actions_to_add.append(get_action_info_dict('user_query_ahjs_is_ahj_official_of', user_query_ahjs_is_ahj_official_of))
admin_actions_to_add.append(get_action_info_dict('user_query_submitted_edits', user_query_submitted_edits))
admin_actions_to_add.append(get_action_info_dict('user_query_approved_edits', user_query_approved_edits))
admin_actions_to_add.append(get_action_info_dict('user_query_submitted_comments', user_query_submitted_comments))
for action in admin_actions_to_add:
    setattr(user_admin_model, action['name'], action['function'])
    user_admin_model.actions.append(action['name'])

user_admin_model.list_display.remove('password')
user_admin_model.list_display.insert(0, user_admin_model.list_display.pop(user_admin_model.list_display.index('UserID')))
user_admin_model.form = UserChangeForm


"""
Customizing AHJ Admin Model:
Adding Admin Actions:
 - Query AHJ Official Users
"""
ahj_admin_model = model_admin_dict['AHJ']['admin_model']
admin_actions_to_add = []
admin_actions_to_add.append(get_action_info_dict('ahj_query_ahj_official_users', ahj_query_ahj_official_users))
for action in admin_actions_to_add:
    setattr(ahj_admin_model, action['name'], action['function'])
    ahj_admin_model.actions.append(action['name'])


"""
Customizing Comment Admin Model:
Adding Admin Actions:
 - Query Submitting Users
"""
comment_admin_model = model_admin_dict['Comment']['admin_model']
admin_actions_to_add = []
admin_actions_to_add.append(get_action_info_dict('comment_query_submitting_users', comment_query_submitting_users))
for action in admin_actions_to_add:
    setattr(comment_admin_model, action['name'], action['function'])
    comment_admin_model.actions.append(action['name'])


"""
Customizing Contact Admin Model:
Removing from list_display:
 - ParentTable
 - ParentID
"""
contact_admin_model = model_admin_dict['Contact']['admin_model']
contact_admin_model.list_display.remove('ParentTable')
contact_admin_model.list_display.remove('ParentID')


"""
Customizing Polygon Admin Model:
Removing from list_display:
 - The Polygon MULTIPOLYGON data field.
"""
polygon_admin_model = model_admin_dict['Polygon']['admin_model']
polygon_admin_model.list_display.remove('Polygon')


"""
Customizing Edit Admin Model:
Adding Admin Actions:
 - Approve Edits
 - Roll back Edits
 - Query Submitting Users
 - Query Approving Users
"""
edit_admin_model = model_admin_dict['Edit']['admin_model']
admin_actions_to_add = []
admin_actions_to_add.append(get_action_info_dict('edit_approve_edits', edit_approve_edits))
admin_actions_to_add.append(get_action_info_dict('edit_roll_back_edits', edit_roll_back_edits))
admin_actions_to_add.append(get_action_info_dict('edit_query_submitting_users', edit_query_submitting_users))
admin_actions_to_add.append(get_action_info_dict('edit_query_approving_users', edit_query_approving_users))
for action in admin_actions_to_add:
    setattr(edit_admin_model, action['name'], action['function'])
    edit_admin_model.actions.append(action['name'])


"""
Register all the admin models to admin site.
"""
for v in model_admin_dict.values():
    admin.site.register(v['model'],v['admin_model'])
