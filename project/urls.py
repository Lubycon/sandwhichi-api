from django.conf.urls import url
from project import views as project_views

app_name = 'project'

project_list = project_views.ProjectViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

project_detail = project_views.ProjectViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy',
})

project_profile_image_patch = project_views.ProjectViewSet.as_view({
    'patch': 'patch_profile_image',
})

project_title_patch = project_views.ProjectViewSet.as_view({
    'patch': 'patch_title',
})

project_descriptions_patch = project_views.ProjectViewSet.as_view({
    'patch': 'patch_descriptions',
})

project_media_patch = project_views.ProjectViewSet.as_view({
    'patch': 'patch_media',
})

urlpatterns = [
    url(r'^projects$', project_list, name='project-list'),
    url(r'^projects/(?P<pk>[0-9]+)$', project_detail, name='project-detail'),
    url(r'^projects/(?P<pk>[0-9]+)/profile-image', project_profile_image_patch, name='project-profile-image-patch'),
    url(r'^projects/(?P<pk>[0-9]+)/title$', project_title_patch, name='project-title-patch'),
    url(r'^projects/(?P<pk>[0-9]+)/descriptions$', project_descriptions_patch, name='project-descriptions-patch'),
    url(r'^projects/(?P<pk>[0-9]+)/media$', project_media_patch, name='project-media-patch'),
    url(r'^projects/questions$', project_views.DescriptionQuestionViewSet.as_view(), name='project-question-list'),
    url(r'^schedules/recurringtypes$', project_views.ScheduleRecurringTypeViewSet.as_view(), name='schedule-recurring-list'),
]