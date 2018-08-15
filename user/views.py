from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView
from user.models import User
from user.serializers import UserSimpleSerializer
from django.shortcuts import get_object_or_404
from base.exceptions import BadRequest


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
        project_object = get_object_or_404(User, pk=kwargs.get('user_id'))
        serializer = UserSimpleSerializer(project_object)

        return Response(serializer.data, status=status.HTTP_200_OK)


class MeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )

    def retrieve(self, request, *args, **kwargs):
        serializer = UserSimpleSerializer(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)