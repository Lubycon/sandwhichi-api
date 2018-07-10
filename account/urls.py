from django.conf.urls import url
from rest_framework_jwt.views import (
    obtain_jwt_token, refresh_jwt_token, verify_jwt_token
)
from user import views as user_views

app_name = 'account'

urlpatterns = [
    url(r'^auth/signin/$', obtain_jwt_token),
    url(r'^auth/signup/$', user_views.Signup.as_view()),
    url(r'^auth/token/refresh/$', refresh_jwt_token),
    url(r'^auth/token/verify/$', verify_jwt_token),
]