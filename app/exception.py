


class BaseAppException(Exception):
    detail = "Internal server error"

class UserAlreadyExistsException(BaseAppException):
    detail = "User with this email or username already exists"

class BadRequestException(BaseAppException):
    detail = "Either the login/password or Google Token is not specified."

class UserNotFoundException(BaseAppException):
    detail = "User not found"

class UserNotCorrectPasswordException(BaseAppException):
    detail = "User not correct password!"

class TokenExpired(BaseAppException):
    detail = "Token has expired"

class TokenNotCorrect(BaseAppException):
    detail = "Token is not correct"

class TaskNotFound(BaseAppException):
    detail = "Task is not found"

class CategoryNotFound(BaseAppException):
    detail = "Category is not found"