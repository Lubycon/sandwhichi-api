from django.conf.urls import url
from rest_framework_jwt.views import (
    obtain_jwt_token, refresh_jwt_token, verify_jwt_token
)

app_name = 'account'

urlpatterns = [
    url(r'^signin$', obtain_jwt_token),
]