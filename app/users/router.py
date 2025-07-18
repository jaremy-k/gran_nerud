from datetime import timedelta

from fastapi import APIRouter, Response, Depends

from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user, get_current_admin_user
from app.users.models import Users
from app.users.shemas import SUsersAuth, SUserAuth

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"]
)


@router.post("/register")
async def register_user(data: SUsersAuth):
    existing_user = await UsersDAO.find_one_or_none(email=data.email)
    if existing_user:
        raise UserAlreadyExistsException

    hashed_password = get_password_hash(data.password)
    await UsersDAO.add({"email": data.email, "hashed_password": hashed_password})


@router.post("/login")
async def login_user(response: Response, user_data: SUsersAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(
        key="tg_news_bot_access_token",
        value=access_token,
        httponly=True,  # Защита от XSS (обязательно)
        secure=True,  # False для localhost (True для HTTPS в продакшене)
        samesite="none",  # "none" не работает без secure=True
        domain="webhooktestjaremyapi.loca.lt",  # Не указываем domain для localhost
        max_age=30 * 24 * 60 * 60,  # 30 дней в секундах (int)
        path="/",  # Доступна для всех путей
    )
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("tg_news_bot_access_token")


@router.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user


@router.get("/all")
async def read_users_all(current_user=Depends(get_current_admin_user)):
    users = await UsersDAO.find_all()
    return users
