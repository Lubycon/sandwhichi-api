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
    'get': 'retrieve'
})

urlpatterns = [
    url(r'users/exists/email/', user_views.IsExistEmailViewSet.as_view(), name='is-exist-email'),
    url(r'^users/$', user_list, name='user-list'),
    url(r'^users/(?P<user_id>[0-9]+)/$', user_detail, name='user-detail'),

    url(r'^users/me/$', my_info, name='my-info'),
]