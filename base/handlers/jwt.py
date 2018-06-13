from datetime import datetime
from calendar import timegm
from rest_framework_jwt.settings import api_settings

def jwt_payload_handler(user):
    # JWT에 담을 정보들
    return {
        'user_id': user.pk,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA,
        'orig_iat': timegm(
            datetime.utcnow().utctimetuple()
        )
    }

def jwt_response_payload_handler(token, user=None, request=None):
    # 인증 후 Response 내용
    return {
        'token': token,
        'user': {
            'id': user.id,
            'email': user.email,
            'username': user.username,
        },
    }