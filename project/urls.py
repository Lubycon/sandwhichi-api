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

project_location_patch = project_views.ProjectViewSet.as_view({
    'patch': 'patch_location',
})

project_date_patch = project_views.ProjectViewSet.as_view({
    'patch': 'patch_date',
})

project_descriptions_patch = project_views.ProjectViewSet.as_view({
    'patch': 'patch_descriptions',
})

project_media_patch = project_views.ProjectViewSet.as_view({
    'patch': 'patch_media',
})

project_schedule_patch = project_views.ProjectViewSet.as_view({
    'patch': 'patch_schedules',
})

project_contact_patch = project_views.ProjectViewSet.as_view({
    'patch': 'patch_contacts'
})

project_abilities = project_views.ProjectViewSet.as_view({
    'post': 'add_ability',
})

project_ability = project_views.ProjectViewSet.as_view({
    'delete': 'remove_ability',
})

project_keywords = project_views.ProjectViewSet.as_view({
    'post': 'add_keyword',
})

project_keyword = project_views.ProjectViewSet.as_view({
    'delete': 'remove_keyword',
})

project_manage_members = project_views.ProjectMemberManageViewSet.as_view({
    'post': 'add_member',
})

project_manage_member = project_views.ProjectMemberManageViewSet.as_view({
    'delete': 'delete_member',
    'patch': 'patch_role',
})

project_manage_owner = project_views.ProjectMemberManageViewSet.as_view({
    'patch': 'appointment_owner',
})

project_requests = project_views.ProjectMemberRequestViewSet.as_view({
    'post': 'create',
    'delete': 'cancel',
})

urlpatterns = [
    url(r'^projects/$', project_list, name='project-list'),
    url(r'^projects/(?P<project_id>[0-9]+)/$', project_detail, name='project-detail'),
    url(r'^projects/(?P<project_id>[0-9]+)/profile-image/$', project_profile_image_patch, name='project-profile-image-patch'),
    url(r'^projects/(?P<project_id>[0-9]+)/title/$', project_title_patch, name='project-title-patch'),
    url(r'^projects/(?P<project_id>[0-9]+)/location/$', project_location_patch, name='project-location-patch'),
    url(r'^projects/(?P<project_id>[0-9]+)/date/$', project_date_patch, name='project-date-patch'),
    url(r'^projects/(?P<project_id>[0-9]+)/descriptions/$', project_descriptions_patch, name='project-descriptions-patch'),
    url(r'^projects/(?P<project_id>[0-9]+)/media/$', project_media_patch, name='project-media-patch'),
    url(r'^projects/(?P<project_id>[0-9]+)/schedules/$', project_schedule_patch, name='project-schedule-patch'),
    url(r'^projects/(?P<project_id>[0-9]+)/contacts/$', project_contact_patch, name='project-contact-patch'),

    url(r'^projects/(?P<project_id>[0-9]+)/abilities/$', project_abilities, name='project-abilities'),
    url(r'^projects/(?P<project_id>[0-9]+)/abilities/(?P<ability_id>[0-9]+)/$', project_ability, name='project-ability'),

    url(r'^projects/(?P<project_id>[0-9]+)/keywords/$', project_keywords, name='project-keywords'),
    url(r'^projects/(?P<project_id>[0-9]+)/keywords/(?P<keyword_id>[0-9]+)/$', project_keyword, name='project-keyword'),

    url(r'^projects/(?P<project_id>[0-9]+)/members/$', project_manage_members, name='project_manage_members'),
    url(r'^projects/(?P<project_id>[0-9]+)/members/(?P<user_id>[0-9]+)/$', project_manage_member, name='project_manage_member'),
    url(r'^projects/(?P<project_id>[0-9]+)/owner/(?P<user_id>[0-9]+)/$', project_manage_owner, name='project_manage_owner'),

    url(r'^projects/(?P<project_id>[0-9]+)/requests/$', project_requests, name='project_requests'),

    url(r'^projects/questions/$', project_views.DescriptionQuestionViewSet.as_view(), name='project-question-list'),
    url(r'^schedules/recurringtypes/$', project_views.ScheduleRecurringTypeViewSet.as_view(), name='schedule-recurring-list'),
]