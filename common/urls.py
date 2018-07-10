from django.conf.urls import url
from common import views as common_views

app_name = 'common'

urlpatterns = [
    url(r'^contacts/types/$', common_views.ContactTypeViewSet.as_view(), name='contact-types'),
    url(r'^media/types/$', common_views.MediaTypeViewSet.as_view(), name='media-types'),
]