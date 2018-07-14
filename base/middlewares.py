from rest_framework.response import Response
from django.http import JsonResponse

def is_registered(exception):
    try:
        return exception.is_error_response
    except AttributeError as e:
        return False

class APIResponseMiddleWare(object):
    """
    API 응답 미들웨어
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if (isinstance(response, Response)):
            data = response.data
            response.data = {
                'results': data,
            }
            response._is_rendered = False
            response.render()
        return response

    def process_exception(self, request, exception):
        if is_registered(exception):
            status = exception.status_code
            exception_dict = exception.to_dict()
        else:
            # @TODO 에러 트래킹 추가
            import traceback
            print(traceback.format_exc())
            status = 500
            exception_dict = { 'message': '알 수 없는 서버 장애입니다. 문제가 계속 될 경우 고객센터로 문의해주세요!' }

        error_message = exception_dict['message']
        return JsonResponse(exception_dict, status=status)