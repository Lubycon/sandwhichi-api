from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.filters import OrderingFilter
from project.models import (
    Project, ScheduleRecurringType, DescriptionQuestion, ProjectDescription
)
from project.serializers import (
    ScheduleRecurringTypeSerializer, DescriptionQuestionSerializer,
    ProjectSaveSerializer, ProjectSerializer, ProjectDescriptionCreateSerializer
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