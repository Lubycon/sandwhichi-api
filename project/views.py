from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.filters import OrderingFilter
from base.exceptions import Conflict, NotFound
from common.models import Ability, Keyword, Contact
from project.models import (
    Project, ScheduleRecurringType,
    DescriptionQuestion, ProjectDescription, Media,
    ProjectMember
)
from location.models import Location
from user.models import User
from project.serializers import (
    ScheduleRecurringTypeSerializer, DescriptionQuestionSerializer,
    ProjectSaveSerializer, ProjectSerializer, ProjectScheduleSaveSerializer,
    ProjectMemberSaveSerializer, ProjectMemberSerializer,
    ProjectMemberRequestSaveSerializer
)
from base.mixins.custom_permissions import (
    PermissionClassesByAction, IsProjectOwner,
)
from base.enums import RequestStatus

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


class ProjectViewSet(PermissionClassesByAction, viewsets.ModelViewSet):
    """
    프로젝트 생성, 리스트, 뷰, 삭제, 패치 API
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = (OrderingFilter, )
    ordering = '-created_at'
    permission_classes_by_action = {
        'list': [AllowAny],
        'retrieve': [AllowAny],
        'default': [IsAuthenticated],
    }


    def create(self, request, *args, **kwargs):
        serializer = ProjectSaveSerializer(request, data=request.data)

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
        project_object = get_object_or_404(Project, pk=kwargs.get('project_id'))
        serializers = ProjectSerializer(project_object)

        return Response(serializers.data, status=status.HTTP_200_OK)


    def destroy(self, request, *args, **kwargs):
        # 프로젝트를 되살려야 할 수도 있기 때문에 프로젝트 모델만 소프트 딜리트 한다
        project_object = get_object_or_404(Project, id=kwargs.get('project_id'))
        project_object.delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def patch_profile_image(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs.get('project_id'))
        new_profile_image = request.data.get('profile_image')
        if not new_profile_image:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        project.profile_image = new_profile_image
        project.save()

        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def patch_title(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs.get('project_id'))
        new_title = request.data.get('title')
        if not new_title:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        project.title = new_title
        project.save()

        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def patch_location(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs.get('project_id'))
        new_location_code = request.data.get('location_code')
        if not new_location_code:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        new_location = get_object_or_404(Location, address_1_code=new_location_code, address_2_code__isnull=True)
        project.location = new_location
        project.save()

        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def patch_date(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs.get('project_id'))
        new_started_at = request.data.get('started_at')
        new_ends_at = request.data.get('ends_at')
        if not new_started_at or not new_ends_at:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        project.started_at = new_started_at
        project.ends_at = new_ends_at
        project.save()

        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def patch_descriptions(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs.get('project_id'))
        descriptions_data = request.data.get('descriptions')
        ProjectDescription.objects.filter(project=project).delete()
        for description_data in descriptions_data:
            description = ProjectDescription(
                project=project,
                question_id=description_data.get('question'),
                answer=description_data.get('answer'),
            )
            description.save()

        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def patch_media(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs.get('project_id'))
        media_data = request.data.get('media')
        project.medai.all().delete()
        for media_data_object in media_data:
            type_data = media_data_object.get('type')
            url_data = media_data_object.get('url')
            media = Media(
                type_id=type_data,
                url=url_data,
            )
            media.save()
            project.media.add(media)

        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def patch_schedules(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs.get('project_id'))
        schedule_data = request.data.get('schedule')
        schedule = project.schedule
        project_serializer = ProjectSerializer(project)
        schedule_serializer = ProjectScheduleSaveSerializer(schedule, data=schedule_data)
        if schedule_serializer.is_valid():
            schedule_serializer.save()
            return Response(project_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(schedule_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def patch_contacts(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs.get('project_id'))
        contacts_data = request.data.get('contacts')
        project.contacts.all().delete()
        for contact_data in contacts_data:
            type_data = contact_data.get('type')
            information_data = contact_data.get('information')
            contact = Contact(
                type_id=type_data,
                information=information_data,
            )
            contact.save()
            project.contacts.add(contact)

        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def add_ability(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs.get('project_id'))
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
        project = get_object_or_404(Project, id=kwargs.get('project_id'))
        ability = get_object_or_404(project.abilities, id=kwargs.get('ability_id'))

        new_count = ability.count - 1
        ability.count = new_count
        ability.save()
        project.abilities.remove(ability)

        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def add_keyword(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs.get('project_id'))
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
        project = get_object_or_404(Project, id=kwargs.get('project_id'))
        keyword = get_object_or_404(project.keywords, id=kwargs.get('keyword_id'))

        new_count = keyword.count - 1
        keyword.count = new_count
        keyword.save()
        project.keywords.remove(keyword)

        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProjectMemberViewSet(viewsets.ViewSet):
    """
    프로젝트 멤버 리스트, 승인, 삭제, 패치 API
    """
    permission_classes = (IsProjectOwner, )

    def add_member(self, request, *args, **kwargs):
        project_id = kwargs.get('project_id')
        project = get_object_or_404(Project, id=project_id)
        user = get_object_or_404(User, id=request.data.get('user'))
        self.check_object_permissions(request, project)

        request.data['project'] = project_id
        serializer = ProjectMemberSaveSerializer(data=request.data)

        if serializer.is_valid():
            project_member = serializer.save()
            project_member_serializer = ProjectMemberSerializer(project_member)

            return Response(project_member_serializer.data, status=status.HTTP_201_CREATED)
        elif serializer.errors.get('already_exist_user'):
            raise Conflict(serializer.errors.get('already_exist_user')[0])
        elif serializer.errors.get('has_not_request'):
            raise NotFound(serializer.errors.get('has_not_request')[0])
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete_member(self, request, *args, **kwargs):
        pass


    def patch_role(self, request, *args, **kwargs):
        project_id = kwargs.get('project_id')
        user_id = kwargs.get('user_id')
        new_role = request.data.get('role')
        project_member = get_object_or_404(ProjectMember, project=project_id, user=user_id, )


class ProjectMemberRequestViewSet(viewsets.ViewSet):
    """
    프로젝트 멤버 신청, 철회 API
    """
    permission_classes = (IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        project_id = kwargs.get('project_id')
        # 404 Exception
        get_object_or_404(Project, id=project_id)

        user = request.user
        data = {
            'project': project_id,
            'user': user.id,
            'status': RequestStatus.REQUESTED.name,
        }

        serializer = ProjectMemberRequestSaveSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({}, status=status.HTTP_201_CREATED, )
        elif serializer.errors.get('already_exist_request'):
            raise Conflict(serializer.errors.get('already_exist_request')[0])
        elif serializer.errors.get('already_exist_member'):
            raise Conflict(serializer.errors.get('already_exist_member')[0])

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, )
