from django.conf.urls import url
from project import views as project_views

app_name = 'project'

project_list = project_views.ProjectViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

project_detail = project_views.ProjectViewSet.as_view({
    'get': 'retrieve',
    'put': 'put',
    'delete': 'destroy',
})

urlpatterns = [
    url(r'^projects$', project_list, name='project-list'),
    url(r'^projects/(?P<pk>[0-9]+)$', project_detail, name='project-detail'),
    url(r'^projects/questions$', project_views.DescriptionQuestionViewSet.as_view()),
    url(r'^schedules/recurringtypes$', project_views.ScheduleRecurringTypeViewSet.as_view()),
]