from bson import ObjectId
from pydantic import BaseModel


class SServices(BaseModel):
    _id: str | None = None
    name: str | None = None

    class Config:
        json_encoders = {ObjectId: str}
