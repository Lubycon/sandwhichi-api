from django.conf.urls import url
from location import views as location_views

app_name = 'location'

location_first_list = location_views.LocationViewSet.as_view({
    'get': 'first_list',
})
location_second_list = location_views.LocationViewSet.as_view({
    'get': 'second_list',
})
location_third_list = location_views.LocationViewSet.as_view({
    'get': 'third_list',
})

urlpatterns = [
    url(r'^locations$', location_first_list, name='location-first-list'),
    url(r'^locations/(?P<address_0_code>[0-9]+)$', location_second_list, name='location-second-list'),
    url(r'^locations/(?P<address_0_code>[0-9]+)/(?P<address_1_code>[0-9]+)$', location_third_list, name='location-third-list'),
]