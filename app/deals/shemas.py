from datetime import datetime
from typing import Optional, Any

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
    deliveryAddressId: str | None = None
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
        populate_by_name = True


class SDealsAdd(BaseModel):
    createdAt: datetime | None = None
    serviceId: str | None = None
    customerId: str | None = None
    stageId: str | None = None
    materialId: str | None = None
    unitMeasurement: str | None = None
    quantity: float | None = None
    methodReceiving: str | None = None
    paymentMethod: str | None = None
    shippingAddressId: str | None = None
    deliveryAddressId: str | None = None
    amountPerUnit: float | None = None
    amountPurchase: float | None = None
    amountDelivery: float | None = None
    companyProfit: float | None = None
    totalAmount: float | None = None
    managerProfit: float | None = None
    deadline: datetime | None = None
    notes: str | None = None
    OSSIG: bool | None = None
    userId: str | None = None

    @field_validator(
        "serviceId", "customerId", "stageId", "materialId",
        "shippingAddressId", "deliveryAddressId", "userId"
    )
    def convert_str_to_objectid(cls, v: Optional[str]) -> Optional[ObjectId]:
        if not v:
            return None
        try:
            return ObjectId(v)
        except Exception:
            raise ValueError(f"Invalid ObjectId format: {v}")

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
