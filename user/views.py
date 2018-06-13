from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.serializers import SignupUserSerializer
from django.contrib.auth import get_user_model

class UserCreate(APIView):
    """
    유저 생성 API
    """

    def post(self, request, format='json'):
        serializer = SignupUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(status=status.HTTP_201_CREATED)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)