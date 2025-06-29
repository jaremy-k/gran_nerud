from bson import ObjectId
from pydantic import BaseModel


class SCompanies(BaseModel):
    _id: str | None = None
    name: str | None = None
    inn: int | None = None
    contacts: dict | None = None

    class Config:
        json_encoders = {ObjectId: str}