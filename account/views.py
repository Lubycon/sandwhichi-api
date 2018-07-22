from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.serializers import SignupUserSerializer
from base.handlers.jwt import get_jwt, jwt_response_payload_handler
from base.exceptions import BadRequest
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework.permissions import IsAuthenticated


class Signup(APIView):
    """
    유저 생성 API
    """

    def post(self, request, format='json'):
        serializer = SignupUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = get_jwt(user)
                response = {
                    'auth_token': token,
                }

                return Response(response, status=status.HTTP_201_CREATED)
        elif serializer.errors.get('email'):
            raise BadRequest('이미 존재하는 이메일입니다. 다른 이메일을 사용해주세요')
        elif serializer.errors.get('password'):
            raise BadRequest('양식에 맞지 않는 비밀번호입니다. 좀 더 복잡한 비밀번호를 사용해주세요.')
        elif serializer.errors.get('has_terms'):
            raise BadRequest('이용약관에 동의해주세요.')
        elif serializer.errors.get('has_privacy_policy'):
            raise BadRequest('개인정보호정책에 동의해주세요.')
        else:
            raise BadRequest('입력하신 정보가 잘못되었습니다. 다시 확인해주세요!')


class Signin(ObtainJSONWebToken):
    """
    로그인 API
    """

    def post(self, request, format='json'):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.object.get('user')
            token = get_jwt(user)
            response_data = jwt_response_payload_handler(token, user, )
            return Response(response_data, status=status.HTTP_200_OK)

        raise BadRequest('회원 정보가 일치하지 않습니다. 이메일 또는 비밀번호를 다시 한번 확인해주세요.')


class PasswordViewSet(APIView):
    """
    비밀번호 인증 API
    """
    permission_classes = (IsAuthenticated, )
    def post(self, request, format='json'):
        user = request.user
        requested_password = request.data.get('password')
        print(user, requested_password)
        if not requested_password:
            raise BadRequest('비밀번호를 입력해주세요.')

        is_valid = user.check_password(requested_password)
        if not is_valid:
            raise BadRequest('비밀번호가 일치하지 않습니다. 다시 한번 확인해주세요')

        return Response({}, status=status.HTTP_200_OK)


