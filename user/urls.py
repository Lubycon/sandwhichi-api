from django.conf.urls import url
from user import views as user_views

app_name = 'user'

user_list = user_views.UserViewSet.as_view({
    'get': 'list',
})
user_detail = user_views.UserViewSet.as_view({
    'get': 'retrieve',
})

my_info = user_views.MeViewSet.as_view({
    'get': 'retrieve',
})
my_abilities = user_views.MeViewSet.as_view({
    'post': 'add_ability',
})
my_ability = user_views.MeViewSet.as_view({
    'delete': 'remove_ability',
})
my_keywords = user_views.MeViewSet.as_view({
    'post': 'add_keyword',
})
my_keyword = user_views.MeViewSet.as_view({
    'delete': 'remove_keyword',
})

urlpatterns = [
    url(r'users/exists/email/', user_views.IsExistEmailViewSet.as_view(), name='is-exist-email'),
    url(r'^users/$', user_list, name='user-list'),
    url(r'^users/(?P<user_id>[0-9]+)/$', user_detail, name='user-detail'),

    url(r'^users/me/$', my_info, name='my-info'),
    url(r'^users/me/abilities/$', my_abilities, name='my-abilities'),
    url(r'^users/me/abilities/(?P<ability_id>[0-9]+)/$', my_ability, name='my-ability'),
    url(r'^users/me/keywords/$', my_keywords, name='my-keywords'),
    url(r'^users/me/keywords/(?P<keyword_id>[0-9]+)/$', my_keyword, name='my-keyword'),
]