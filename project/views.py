from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from project.models import (
    Project, ScheduleRecurringType, DescriptionQuestion
)
from project.serializers import (
    ScheduleRecurringTypeSerializer, DescriptionQuestionSerializer,
    ProjectSaveSerializer, ProjectSerializer
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
    프로젝트 생성, 리스트, 뷰, 삭제 API
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def create(self, request, *args, **kwargs):
        serializer = ProjectSaveSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save()
            if project:
                return Response({}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request, *args, **kwargs):
        pass

    def retrieve(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs.get('pk'))
        serializers = ProjectSerializer(project)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        # project = get_object_or_404(Project, pk=kwargs.get('pk'))
        return Response({}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs.get('pk'))
        print(project)
        project.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
