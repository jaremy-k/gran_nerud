from fastapi import HTTPException, status


class TgUserException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(TgUserException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class IncorrectEmailOrPasswordException(TgUserException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"


class TokenExpireException(TgUserException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен истек"


class TokenAbsentException(TgUserException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenFormatEcxeption(TgUserException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIsNotPresentException(TgUserException):
    status_code = status.HTTP_401_UNAUTHORIZED