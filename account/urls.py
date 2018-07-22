from django.conf.urls import url
from rest_framework_jwt.views import (
    refresh_jwt_token, verify_jwt_token
)
from account import views as account_views

app_name = 'account'

urlpatterns = [
    url(r'^auth/signin/$', account_views.Signin.as_view()),
    url(r'^auth/signup/$', account_views.Signup.as_view()),
    url(r'^auth/token/refresh/$', refresh_jwt_token),
    url(r'^auth/token/verify/$', verify_jwt_token),
    url(r'^auth/password/verify/$', account_views.PasswordViewSet.as_view()),
    url(r'^auth/password/token/verify/$', account_views.PasswordChangeTokenViewSet.as_view()),
    url(r'^auth/password/change/$', account_views.PasswordChangeViewSet.as_view()),
]