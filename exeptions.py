class UserNotFoundException(Exception):
    detail = 'User not found'


class UserNotCorrectPasswordException(Exception):
    detail = 'Incorrect password'


class TokenExpiredException(Exception):
    detail = 'Token expired'


class TokenNotValidException(Exception):
    detail = 'Token not valid'


class TaskNotFoundException(Exception):
    detail = 'Task not found'