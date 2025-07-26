from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field, field_validator


class SDeals(BaseModel):
    id: str | None = Field(None, alias="_id")
    serviceId: str | None = None
    createdAt: datetime | None = None
    customerId: str | None = None
    stageId: str | None = None
    materialId: str | None = None
    unitMeasurement: str | None = None
    quantity: float | None = None
    methodReceiving: str | None = None
    paymentMethod: str | None = None
    shippingAddressId: str | None = None
    deliveryAddresslId: str | None = None
    amountPurchase: float | None = None
    amountDelivery: float | None = None
    companyProfit: float | None = None
    totalAmount: float | None = None
    managerProfit: float | None = None
    deadline: datetime | None = None
    notes: str | None = None
    OSSIG: bool | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
    is_deleted: bool | None = None
    userId: str | None = None

    @field_validator("*", mode="before")
    def convert_all_objectids(cls, v, field):
        if isinstance(v, ObjectId):
            return str(v)
        # Для полей, которые могут содержать ObjectId в списке/словаре
        if isinstance(v, list):
            return [str(i) if isinstance(i, ObjectId) else i for i in v]
        if isinstance(v, dict):
            return {k: str(val) if isinstance(val, ObjectId) else val for k, val in v.items()}
        return v

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True


class SDealsAdd(BaseModel):
    serviceId: ObjectId | None = None
    customerId: ObjectId | None = None
    stageId: ObjectId | None = None
    materialId: ObjectId | None = None
    unitMeasurement: str | None = None
    quantity: float | None = None
    methodReceiving: str | None = None
    paymentMethod: str | None = None
    shippingAddressId: ObjectId | None = None
    deliveryAddresslId: ObjectId | None = None
    amountPerUnit: float | None = None
    amountPurchase: float | None = None
    amountDelivery: float | None = None
    companyProfit: float | None = None
    totalAmount: float | None = None
    managerProfit: float | None = None
    deadline: datetime | None = None
    notes: str | None = None
    OSSIG: bool | None = None
    userId: ObjectId | None = None

    @field_validator('*', mode='before')
    def validate_objectid_fields(cls, v, info):
        if info.field_name in ['serviceId', 'customerId', 'stageId',
                               'materialId', 'shippingAddressId',
                               'deliveryAddressId', 'userId']:
            if v is None:
                return None
            if isinstance(v, ObjectId):
                return v
            try:
                return ObjectId(v)
            except Exception:
                raise ValueError(f"Invalid ObjectId for field {info.field_name}: {v}")
        return v

    class Config:
        json_encoders = {ObjectId: str}
        from_attributes = True
        populate_by_name = True


class SDealsWithRelations(SDeals):
    service: Optional[dict] = None
    customer: Optional[dict] = None
    stage: Optional[dict] = None
    material: Optional[dict] = None
    shipping_address: Optional[dict] = None
    delivery_address: Optional[dict] = None
    user: Optional[dict] = None

    @field_validator("id", mode="before")
    def convert_objectid(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    class Config:
        json_encoders = {ObjectId: str}
