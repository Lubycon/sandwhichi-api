from django.conf.urls import url
from location import views as location_views

app_name = 'project'

urlpatterns = [
    url(r'^locations$', location_views.LocationViewSet.as_view(), name='location-list'),
]