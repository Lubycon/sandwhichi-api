from django.conf.urls import url
from project import views as project_views

app_name = 'project'

urlpatterns = [
    url(r'^schedules/recurringtypes$', project_views.ScheduleRecurringTypeViewSet.as_view()),
    url(r'^projects$', project_views.ProjectViewSet.as_view()),
    url(r'^projects/questions$', project_views.DescriptionQuestionViewSet.as_view()),
]