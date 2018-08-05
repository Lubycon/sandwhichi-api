from django.conf.urls import url
from user import views as user_views

app_name = 'user'

user_list = user_views.UserViewSet.as_view({
    'get': 'list',
})
user_detail = user_views.UserViewSet.as_view({
    'get': 'retrieve',
})

urlpatterns = [
    url(r'^users/$', user_list, name='user-list'),
    url(r'^users/(?P<user_id>[0-9]+)/$', user_detail, name='user-detail'),
]