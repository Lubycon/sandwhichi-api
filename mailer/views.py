from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from base.helpers import email_helper
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class PasswordChange(APIView):
    """
    비밀번호 변경 이메일 발송
    """
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        user = request.user
        user_email = user.email
        template_path = 'email/password_change/password_change'

        token = PasswordResetTokenGenerator().make_token(user)
        redirect_url = '/auth/password/landing/%s' % (token)

        context = {
            'username': user.username,
            'redirect_url': redirect_url,
        }

        email_result = email_helper.email_send(
            request,
            to_address=user_email,
            template_path=template_path,
            context=context
        )

        result_data = {
            'email': email_result,
        }

        return Response(result_data, status=status.HTTP_200_OK)


class EmailCertification(APIView):
    """
    이메일 주소 인증 이메일 발송
    """
    permission_classes = (IsAuthenticated, )
    def post(self, request):
        user = request.user
        user_email = user.email
        template_path = 'email/email_certification/email_certification'

        token = PasswordResetTokenGenerator().make_token(user)
        redirect_url = '/auth/%s' % (token)

        context = {
            'username': user.username,
            'redirect_url': redirect_url,
        }

        email_result = email_helper.email_send(
            request,
            to_address=user_email,
            template_path=template_path,
            context=context
        )

        result_data = {
            'email': email_result,
        }

        return Response(result_data, status=status.HTTP_200_OK)