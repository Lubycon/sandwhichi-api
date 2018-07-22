from django.conf.urls import url
from mailer import views as mailer_views

app_name = 'mailer'

urlpatterns = [
    url(r'^mail/password/change/$', mailer_views.PasswordChange.as_view()),
]