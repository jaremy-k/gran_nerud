from bson import ObjectId
from pydantic import BaseModel, EmailStr


class SUsersAuth(BaseModel):
    email: EmailStr
    password: str

    class Config:
        json_encoders = {ObjectId: str}


class SUserAuth(BaseModel):
    email: EmailStr
    hashed_password: str

    class Config:
        json_encoders = {ObjectId: str}


class SUsersGet(BaseModel):
    name: str
    lastName: str
    fatherName: str
    email: str
    admin: bool

    class Config:
        json_encoders = {ObjectId: str}
