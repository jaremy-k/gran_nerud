from datetime import datetime, timedelta
from passlib.context import CryptContext
from pydantic import EmailStr
from jose import jwt

from app.config import settings
from app.logger import logger
from app.users.dao import UsersDAO
from app.users.shemas import SUsersGet

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITHM
    )
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str):
    user_dict = await UsersDAO.find_one_or_none(email=email)
    user = SUsersGet.model_validate(user_dict)
    if not (user and verify_password(password, user.hashed_password)):
        return None
    return user
