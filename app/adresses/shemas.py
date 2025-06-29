from bson import ObjectId
from pydantic import BaseModel


class SAdresses(BaseModel):
    _id: str | None = None
    companyId: str | None = None
    coordinates: list | None = None
    cityId: str | None = None
    adressDetail: dict | None = None
    typeAdress: str | None = None

    class Config:
        json_encoders = {ObjectId: str}