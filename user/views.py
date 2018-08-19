from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView
from user.models import User
from user.serializers import UserSimpleSerializer
from django.shortcuts import get_object_or_404
from base.exceptions import BadRequest
from django.core.exceptions import ObjectDoesNotExist
from common.models import Ability, Keyword
from project.models import ProjectMember


class IsExistEmailViewSet(APIView):
    """
    이메일 존재 여부 확인 API
    """
    def post(self, request, format='json'):
        email = request.data.get('email')

        if not email:
            BadRequest('이메일 주소를 입력해주세요')

        is_exist = User.objects.filter(email=email).exists()
        return Response({ 'is_exist': is_exist }, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """
    유저 리스트, 유저 디테일 API
    """
    queryset = User.objects.all()
    serializer_class = UserSimpleSerializer
    filter_backends = (OrderingFilter,)
    ordering = '-created_at'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True, )
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs.get('user_id'))
        serializer = UserSimpleSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # def get_projects(self, request, *args, **kwargs):
    #     user = get_object_or_404(User, pk=kwargs.get('user_id'))
    #     my_projects = ProjectMember.objects.filter(user=user, is_active=True, )
    #     serializer = UserProjectSerializer(my_projects, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


class MeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )

    def retrieve(self, request, *args, **kwargs):
        serializer = UserSimpleSerializer(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def add_ability(self, request, *args, **kwargs):
        me = request.user
        my_profile = me.profile
        ability_string = request.data.get('ability')
        try:
            my_profile.abilities.get(name=ability_string)
            return Response({}, status=status.HTTP_409_CONFLICT)
        except ObjectDoesNotExist:
            ability, created = Ability.objects.get_or_create(name=ability_string)
            new_count = ability.count + 1
            ability.count = new_count
            ability.save()
            my_profile.abilities.add(ability)

            serializer = UserSimpleSerializer(me)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def remove_ability(self, request, *args, **kwargs):
        me = request.user
        my_profile = me.profile
        ability = get_object_or_404(my_profile.abilities, id=kwargs.get('ability_id'))

        new_count = ability.count - 1
        ability.count = new_count
        ability.save()
        my_profile.abilities.remove(ability)

        serializer = UserSimpleSerializer(me)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def add_keyword(self, request, *args, **kwargs):
        me = request.user
        my_profile = me.profile
        keyword_string = request.data.get('keyword')
        try:
            my_profile.keywords.get(name=keyword_string)
            return Response({}, status=status.HTTP_409_CONFLICT)
        except ObjectDoesNotExist:
            keyword, created = Keyword.objects.get_or_create(name=keyword_string)
            new_count = keyword.count + 1
            keyword.count = new_count
            keyword.save()
            my_profile.keywords.add(keyword)

            serializer = UserSimpleSerializer(me)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def remove_keyword(self, request, *args, **kwargs):
        me = request.user
        my_profile = me.profile
        keyword = get_object_or_404(my_profile.keywords, id=kwargs.get('keyword_id'))

        new_count = keyword.count - 1
        keyword.count = new_count
        keyword.save()
        my_profile.keywords.remove(keyword)

        serializer = UserSimpleSerializer(me)
        return Response(serializer.data, status=status.HTTP_200_OK)