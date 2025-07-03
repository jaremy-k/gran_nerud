from bson import ObjectId
from pydantic import BaseModel, Field, field_validator


class SMaterials(BaseModel):
    id: str | None = Field(None, alias="_id")
    name: str | None = None

    @field_validator("id", mode="before")
    def convert_objectid(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    class Config:
        json_encoders = {ObjectId: str}


class SMaterialsAdd(BaseModel):
    name: str | None = None

    class Config:
        json_encoders = {ObjectId: str}
        from_attributes = True
        populate_by_name = True
