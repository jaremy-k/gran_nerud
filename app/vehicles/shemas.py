from bson import ObjectId
from pydantic import BaseModel


class SVehicles(BaseModel):
    _id: str | None = None
    companyId: str | None = None
    number: str | None = None
    region: int | None = None
    mark: str | None = None
    model: str | None = None
    year: int | None = None
    color: str | None = None

    class Config:
        json_encoders = {ObjectId: str}