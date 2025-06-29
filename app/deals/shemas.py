from datetime import datetime
from decimal import Decimal

from bson import ObjectId
from pydantic import BaseModel


class SDeals(BaseModel):
    _id: str | None = None
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
    amountPurchase: Decimal | None = None
    amountDelivery: Decimal | None = None
    companyProfit: Decimal | None = None
    totalAmount: Decimal | None = None
    managerProfit: Decimal | None = None
    deadline: datetime | None = None
    notes: str | None = None
    OSSIG: bool | None = None
    updated_at: datetime | None = None

    class Config:
        json_encoders = {ObjectId: str}