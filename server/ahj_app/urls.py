from django.urls import path, include
from . import views_ahjsearch, views_ahjsearch_api, views_users, views_misc, views_edits, views_datavis


urlpatterns = [
    path('ahj/',                          views_ahjsearch_api.ahj_list,                            name='ahj-public'),
    path('ahj-private/',                  views_ahjsearch.webpage_ahj_list,                        name='ahj-private'),
    path('geo/address/',                  views_ahjsearch_api.ahj_geo_address,                     name='ahj-geo-address'),
    path('geo/location/',                 views_ahjsearch_api.ahj_geo_location,                    name='ahj-geo-location'),
    path('ahj-one/',                      views_ahjsearch.get_single_ahj,                          name='single_ahj'),
    path('ahj/set-maintainer/',           views_users.set_ahj_maintainer,                          name='ahj-set-maintainer'),
    path('ahj/remove-maintainer/',        views_users.remove_ahj_maintainer,                       name='ahj-remove-maintainer'),
    path('edit/',                         views_edits.edit_list,                                   name='edit-list'),
    path('auth/api-token/create/',        views_users.create_api_token,                            name='create-api-token'),
    path('edit/review/',                  views_edits.edit_review,                                 name='edit-review'),
    path('edit/update/',                  views_edits.edit_update,                                 name='edit-update'),
    path('edit/add/',                     views_edits.edit_addition,                               name='edit-addition'),
    path('edit/delete/',                  views_edits.edit_deletion,                               name='edit-deletion'),
    path('user/update/<str:username>/',   views_users.user_update,                                 name='user-update'),
    path('user/edits/',                   views_misc.user_edits,                                   name='user-edits'),
    path('user/comments/',                views_misc.user_comments,                                name='user-comments'),
    path('user-one/<str:username>/',      views_users.get_single_user,                             name='single-user-info'),
    path('ahj/comment/submit/',           views_misc.comment_submit,                               name="comment-submit"),
    path('data-vis/data-map/',            views_datavis.data_map,                                  name='data-map'),
    path('data-vis/data-map/polygon/',    views_datavis.data_map_get_polygon,                      name='data-map-polygon'),
    path('auth/form-validator/',          views_misc.form_validator,                               name='form-validator'),
    path('auth/users/',                   views_users.RegisterUser.as_view({'post': 'create'}),    name='user-create'),
    path('auth/token/login/',             views_users.LoginUser.as_view(),                         name='user-login'),
    path('auth/token/logout/',            views_users.LogoutUser.as_view(),                        name='user-logout'),
    path('auth/users/activation/',        views_users.ActivateUser.as_view({'post': 'activation'}),                        name='user-activate'),
    path('auth/',                         include('djoser.urls')),
    path('auth/',                         include('djoser.urls.authtoken'))
]
