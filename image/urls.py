from django.conf.urls import url
from image import views as image_views

app_name = 'image'

urlpatterns = [
    url(r'^images/$', image_views.ImageViewSet.as_view(), name='image'),
]