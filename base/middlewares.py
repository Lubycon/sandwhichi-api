from rest_framework.response import Response

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
            print(response.data)
            response._is_rendered = False
            response.render()
        return response