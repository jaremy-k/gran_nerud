from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, Field, field_validator


class SStages(BaseModel):
    id: str | None = Field(None, alias="_id")
    name: str | None = None
    deleted_at: datetime | None = None
    is_deleted: bool | None = None

    @field_validator("id", mode="before")
    def convert_objectid(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    class Config:
        json_encoders = {ObjectId: str}


class SStagesAdd(BaseModel):
    name: str | None = None

    class Config:
        json_encoders = {ObjectId: str}
        from_attributes = True
        populate_by_name = True
