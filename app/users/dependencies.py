from fastapi import Request, Depends

from jose import jwt, JWTError

from app.config import settings
from app.exceptions import TokenAbsentException, IncorrectTokenFormatEcxeption, UserIsNotPresentException
from app.users.dao import UsersDAO


def get_token(request: Request):
    token = request.cookies.get("tg_news_bot_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise IncorrectTokenFormatEcxeption
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    user = await UsersDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise UserIsNotPresentException
    return user


async def get_current_admin_user(current_user=Depends(get_current_user)):
    if not current_user.admin:
        raise UserIsNotPresentException
    return current_user
