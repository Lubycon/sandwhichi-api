from datetime import datetime
from calendar import timegm
from rest_framework_jwt.settings import api_settings

def jwt_payload_handler(user):
    """
    JWT에 담을 정보들
    """
    return {
        'user_id': user.pk,
        'email': user.email,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA,
        'orig_iat': timegm(
            datetime.utcnow().utctimetuple()
        )
    }

def jwt_response_payload_handler(token, user=None, request=None):
    """
    토큰 인증 후 Response 내용
    """
    return {
        'auth_token': token,
        'user': {
            'id': user.id,
            'email': user.email,
            'username': user.username,
        },
    }

def jwt_get_username_from_payload_handler(payload):
    """
    토큰에서 유저를 판별할 값
    """
    return payload.get('email')
    
def get_jwt(user):
    """
    User를 기반으로 JWT를 생성 후 리턴
    """
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    jwt_payload = jwt_payload_handler(user)
    token = jwt_encode_handler(jwt_payload)

    return token