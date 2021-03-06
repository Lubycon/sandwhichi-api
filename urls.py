"""sandwhichi_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='Sandwhichi API')

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^swagger$', schema_view),
    url(r'^', include('account.urls', namespace='account')),
    url(r'^', include('common.urls', namespace='common')),
    url(r'^', include('project.urls', namespace='project')),
    url(r'^', include('location.urls', namespace='location')),
    url(r'^', include('mailer.urls', namespace='mailer')),
    url(r'^', include('image.urls', namespace='image')),
    url(r'^', include('user.urls', namespace='user')),
]
