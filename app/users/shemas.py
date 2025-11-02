from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, field_validator


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
    id: str | None = Field(None, alias="_id")
    name: str | None = None
    lastName: str | None = None
    fatherName: str | None = None
    email: str | None = None
    profit: dict | None = None
    admin: bool | None = False
    hashed_password: str | None = None
    deletedAt: datetime | None = None
    isDeleted: bool | None = None

    @field_validator("id", mode="before")
    def convert_objectid(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    class Config:
        from_attributes = True
        populate_by_name = True
