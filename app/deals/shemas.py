from datetime import datetime
from decimal import Decimal

from bson import ObjectId, Decimal128
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
    amountPurchase: Decimal128 | None = None
    amountDelivery: Decimal128 | None = None
    companyProfit: Decimal128 | None = None
    totalAmount: Decimal128 | None = None
    managerProfit: Decimal128 | None = None
    deadline: datetime | None = None
    notes: str | None = None
    OSSIG: bool | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
    is_deleted: bool | None = None
    userId: str | None = None

    @field_validator("id", mode="before")
    def convert_objectid(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    class Config:
        json_encoders = {ObjectId: str}


class SDealsAdd(BaseModel):
    serviceId: str | None = None
    customerId: str | None = None
    stageId: str | None = None
    materialId: str | None = None
    unitMeasurement: str | None = None
    quantity: float | None = None
    methodReceiving: str | None = None
    paymentMethod: str | None = None
    shippingAddressId: str | None = None
    deliveryAddresslId: str | None = None
    amountPerUnit: Decimal128 | None = None
    amountPurchase: Decimal128 | None = None
    amountDelivery: Decimal128 | None = None
    companyProfit: Decimal128 | None = None
    totalAmount: Decimal128 | None = None
    managerProfit: Decimal128 | None = None
    deadline: datetime | None = None
    notes: str | None = None
    OSSIG: bool | None = None
    userId: str | None = None

    class Config:
        json_encoders = {ObjectId: str}
        from_attributes = True
        populate_by_name = True
