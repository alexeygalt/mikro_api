class UserNotFoundException(Exception):
    detail = 'User not found'


class UserNotCorrectPasswordException(Exception):
    detail = 'Incorrect password'
