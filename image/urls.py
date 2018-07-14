from django.conf.urls import url
from image import views as image_views

app_name = 'image'

urlpatterns = [
    url(r'^contacts/types/$', image_views.ImageViewSet.as_view(), name='image'),
]