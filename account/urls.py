from django.conf.urls import url
from rest_framework_jwt.views import (
    obtain_jwt_token, refresh_jwt_token, verify_jwt_token
)
from user import views as user_views

app_name = 'account'

urlpatterns = [
    url(r'^signin$', obtain_jwt_token),
    url(r'^signup$', user_views.UserCreate.as_view()),
]