class BaseCustomException(Exception):
    status_code = None
    error_message = None
    is_error_response = True

    def __init__(self, error_message):
        Exception.__init__(self)
        self.error_message = error_message

    def to_dict(self):
        return { 'message': self.error_message }

class InternalServerError(BaseCustomException):
    status_code = 500

class BadRequest(BaseCustomException):
    status_code = 400

class BadFileRequest(BaseCustomException):
    status_code = 422

class Conflict(BaseCustomException):
    status_code = 409