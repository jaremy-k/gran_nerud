from datetime import datetime
from typing import Optional, Any, List

from bson import ObjectId
from pydantic import BaseModel, field_validator, ConfigDict
from pydantic.alias_generators import to_camel

from app.base_schemas import PyObjectId, BaseMongoModel


class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )


class PaginationParams(BaseMongoModel):
    page: int = 1
    page_size: int = 100

    @property
    def skip(self) -> int:
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        return self.page_size


class SDeals(BaseModel):
    createdAt: datetime | None = None
    userId: Optional[PyObjectId] = None  # менеджер
    serviceId: Optional[PyObjectId] = None  # тпа услуги
    customerId: Optional[PyObjectId] = None  # заказчик - из companies
    stageId: Optional[PyObjectId] = None  # этап сделки
    materialId: Optional[PyObjectId] = None  # материал
    unitMeasurement: Optional[PyObjectId] = None  # единица измерения

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
