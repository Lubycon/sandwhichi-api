from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.filters import OrderingFilter
from common.models import Ability, Keyword
from project.models import (
    Project, ScheduleRecurringType, DescriptionQuestion, ProjectDescription,
    Media
)
from project.serializers import (
    ScheduleRecurringTypeSerializer, DescriptionQuestionSerializer,
    ProjectSaveSerializer, ProjectSerializer, ScheduleSaveSerializer
)

class ScheduleRecurringTypeViewSet(APIView):
    """
    스케줄 타입 리스트 API
    """

    def get(self, request, format='json'):
        recurringTypes = ScheduleRecurringType.objects.all()
        serializer = ScheduleRecurringTypeSerializer(recurringTypes, many=True, )
        return Response(serializer.data, status=status.HTTP_200_OK)


class DescriptionQuestionViewSet(APIView):
    """
    프로젝트 질문 리스트 API
    """

    def get(self, request, format='json'):
        questions = DescriptionQuestion.objects.all()
        serializer = DescriptionQuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProjectViewSet(viewsets.ModelViewSet):
    """
    프로젝트 생성, 리스트, 뷰, 삭제, 패치 API
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = (OrderingFilter,)
    ordering = '-created_at'

    def create(self, request, *args, **kwargs):
        serializer = ProjectSaveSerializer(data=request.data)

        if serializer.is_valid():
            project = serializer.save()
            project_object = ProjectSerializer(project)
            if project_object:
                return Response(project_object.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True, )
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, )
        return Response(serializer.data, status=status.HTTP_200_OK)


    def retrieve(self, request, *args, **kwargs):
        project_object = get_object_or_404(Project, pk=kwargs.get('pk'))
        serializers = ProjectSerializer(project_object)

        return Response(serializers.data, status=status.HTTP_200_OK)


    def destroy(self, request, *args, **kwargs):
        project_object = get_object_or_404(Project, id=kwargs.get('pk'))
        project_object.delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def patch_profile_image(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs.get('pk'))
        new_profile_image = request.data.get('profile_image')
        if not new_profile_image:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        project.profile_image = new_profile_image
        project.save()

        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def patch_title(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs.get('pk'))
        new_title = request.data.get('title')

        if not new_title:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        project.title = new_title
        project.save()

        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def patch_descriptions(self, request, *args, **kwargs):
        # id값 없는 애들 지워줘야함
        project = get_object_or_404(Project, id=kwargs.get('pk'))
        descriptions_data = request.data.get('descriptions')
        for description_data in descriptions_data:
            description_id = description_data.get('id')
            if description_id:
                description = get_object_or_404(ProjectDescription, id=description_id)
                description.question_id = description_data.get('question')
                description.answer = description_data.get('answer')
            else:
                description = ProjectDescription(
                    project=project,
                    question_id=description_data.get('question'),
                    answer=description_data.get('answer'),
                )
            description.save()

        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def patch_media(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs.get('pk'))
        media_data = request.data.get('media')
        for media_data_object in media_data:
            media_id = media_data_object.get('id')
            if media_id:
                media = get_object_or_404(Media, id=media_id)
                media.type_id = media_data_object.get('type')
                media.url = media_data_object.get('url')
                media.save()
            else:
                media = Media(
                    type_id=media_data_object.get('type'),
                    url=media_data_object.get('url'),
                )
                media.save()
                project.media.add(media)

        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def patch_schedule(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs.get('pk'))
        schedule_data = request.data.get('schedule')
        schedule = project.schedule
        project_serializer = ProjectSerializer(project)
        schedule_serializer = ScheduleSaveSerializer(schedule, data=schedule_data)
        if schedule_serializer.is_valid():
            schedule_serializer.save()
            return Response(project_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(schedule_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        return Response({}, status=status.HTTP_200_OK)

    def add_ability(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs.get('pk'))
        ability_string = request.data.get('ability')
        try:
            project.abilities.get(name=ability_string)
            return Response({}, status=status.HTTP_409_CONFLICT)
        except ObjectDoesNotExist:
            ability, created = Ability.objects.get_or_create(name=ability_string)
            new_count = ability.count + 1
            ability.count = new_count
            ability.save()
            project.abilities.add(ability)

            serializer = ProjectSerializer(project)
            return Response(serializer.data, status=status.HTTP_200_OK)


    def remove_ability(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs.get('pk'))
        ability = get_object_or_404(project.abilities, id=kwargs.get('ability_id'))

        new_count = ability.count - 1
        ability.count = new_count
        ability.save()
        project.abilities.remove(ability)

        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def add_keyword(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs.get('pk'))
        keyword_string = request.data.get('keyword')
        try:
            project.keywords.get(name=keyword_string)
            return Response({}, status=status.HTTP_409_CONFLICT)
        except ObjectDoesNotExist:
            keyword, created = Keyword.objects.get_or_create(name=keyword_string)
            new_count = keyword.count + 1
            keyword.count = new_count
            keyword.save()
            project.keywords.add(keyword)

            serializer = ProjectSerializer(project)
            return Response(serializer.data, status=status.HTTP_200_OK)


    def remove_keyword(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs.get('pk'))
        keyword = get_object_or_404(project.keywords, id=kwargs.get('keyword_id'))

        new_count = keyword.count - 1
        keyword.count = new_count
        keyword.save()
        project.keywords.remove(keyword)

        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

