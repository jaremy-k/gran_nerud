from pydantic import BaseModel, EmailStr


class SUserAuth(BaseModel):
    email: EmailStr
    password: str


class SUsersAuth(BaseModel):
    email: str
    admin: bool
