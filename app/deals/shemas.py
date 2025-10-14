from datetime import datetime
from typing import Optional, Any

from bson import ObjectId
from pydantic import BaseModel, Field, field_validator


class SDeals(BaseModel):
    id: str | None = Field(None, alias="_id")
    createdAt: datetime | None = None
    userId: str | None = None  # менеджер
    serviceId: str | None = None  # тпа услуги
    customerId: str | None = None  # заказчик - из companies
    stageId: str | None = None  # этап сделки
    materialId: str | None = None  # материал
    unitMeasurement: str | None = None  # единица измерения

    # финансовые параметры для расчета
    # итоговая сумма = цена продажи + цена доставки
    quantity: float | None = None  # количество материала (вручную)

    amountPurchaseUnit: float | None = None  # цена за единицу товара (вручную)
    amountPurchaseTotal: float | None = None  # цена закупки (количество * цена за единицу) - динамическое

    amountSalesUnit: float | None = None  # цена за единицу товара (вручную)
    amountSalesTotal: float | None = None  # цена закупки (количество * цена за единицу) - динамическое

    amountDelivery: float | None = None  # цена доставки (вручную)
    companyProfit: float | None = None  # маржа фирмы (цена продажи - цена закупки - цена доставка) (динамическая)

    totalAmount: float | None = None  # общая сумма для заказчика (цена продажи + цена доставки) (динамическая)
    managerProfit: float | None = None  # процент менеджеру (процент менеджера * маржа фирмы) (динамическое)

    paymentMethod: str | None = None  # способ оплаты заказчиком (нал, без нал)
    # адреса
    shippingAddress: str | None = None  # адрес откгрузки (откуда будут забирать товар)
    methodReceiving: str | None = None  # способ получения (доставка, самовывоз)
    deliveryAddress: str | None = None  # адрес доставка (куда доставить товар)

    deadline: datetime | None = None  # срок к которому надо завершить заказ
    notes: str | None = None
    OSSIG: bool | None = None  # это для утилизации

    updatedAt: datetime | None = None
    deletedAt: datetime | None = None

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
    userId: str | None = None  # менеджер
    serviceId: str | None = None  # тпа услуги
    customerId: str | None = None  # заказчик - из companies
    stageId: str | None = None  # этап сделки
    materialId: str | None = None  # материал
    unitMeasurement: str | None = None  # единица измерения

    # финансовые параметры для расчета
    # итоговая сумма = цена продажи + цена доставки
    quantity: float | None = None  # количество материала (вручную)

    amountPurchaseUnit: float | None = None  # цена за единицу товара (вручную)
    amountPurchaseTotal: float | None = None  # цена закупки (количество * цена за единицу) - динамическое

    amountSalesUnit: float | None = None  # цена за единицу товара (вручную)
    amountSalesTotal: float | None = None  # цена закупки (количество * цена за единицу) - динамическое

    amountDelivery: float | None = None  # цена доставки (вручную)
    companyProfit: float | None = None  # маржа фирмы (цена продажи - цена закупки - цена доставка) (динамическая)

    totalAmount: float | None = None  # общая сумма для заказчика (цена продажи + цена доставки) (динамическая)
    managerProfit: float | None = None  # процент менеджеру (процент менеджера * маржа фирмы) (динамическое)

    paymentMethod: str | None = None  # способ оплаты заказчиком (нал, без нал)
    # адреса
    shippingAddress: str | None = None  # адрес откгрузки (откуда будут забирать товар)
    methodReceiving: str | None = None  # способ получения (доставка, самовывоз)
    deliveryAddress: str | None = None  # адрес доставка (куда доставить товар)

    deadline: datetime | None = None  # срок к которому надо завершить заказ
    notes: str | None = None
    OSSIG: bool | None = None  # это для утилизации

    @field_validator(
        "serviceId", "customerId", "stageId", "materialId", "userId"
        # "shippingAddressId", "deliveryAddressId"
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
