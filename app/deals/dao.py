from typing import Optional, Dict, List, Any

from bson import ObjectId

from app.dao.base import MongoDAO
from app.database import database_mongo
from app.deals.shemas import PaginatedResponse
from app.logger import logger


class DealsDAO(MongoDAO):
    collection = database_mongo["deals"]

    @classmethod
    async def find_paginated1(
            cls,
            filter_by: Optional[Dict] = None,
            projection: Optional[Dict] = None,
            skip: int = 0,
            limit: int = 100,
            sort: Optional[List[tuple]] = None,
            include_relations: bool = False,  # Новый параметр
            **kwargs,
    ) -> PaginatedResponse:
        """Find documents with pagination metadata."""
        try:
            query = filter_by or {}
            query.update(kwargs)

            if include_relations:
                # Используем агрегацию для загрузки связанных объектов
                return await cls._find_paginated_with_relations(
                    query=query,
                    skip=skip,
                    limit=limit,
                    sort=sort
                )
            else:
                # Стандартный подход без связей
                return await cls._find_paginated_simple(
                    query=query,
                    projection=projection,
                    skip=skip,
                    limit=limit,
                    sort=sort
                )

        except Exception as e:
            logger.error(f"Error finding paginated documents: {str(e)}", exc_info=True)
            return PaginatedResponse(
                items=[],
                total=0,
                page=1,
                page_size=limit,
                total_pages=0,
                has_next=False,
                has_prev=False
            )

    @classmethod
    async def _find_paginated_simple(
            cls,
            query: Dict,
            projection: Optional[Dict] = None,
            skip: int = 0,
            limit: int = 100,
            sort: Optional[List[tuple]] = None,
    ) -> PaginatedResponse:
        """Простая пагинация без связанных объектов"""
        # Получаем общее количество документов
        total = await cls.collection.count_documents(query)

        # Получаем данные с пагинацией
        cursor = cls.collection.find(query, projection)

        if sort:
            cursor = cursor.sort(sort)

        cursor = cursor.skip(skip).limit(limit)
        items = [doc async for doc in cursor]

        # Конвертируем ObjectId в строки для сериализации
        items = cls._convert_objectids_to_str(items)

        # Вычисляем метаданные пагинации
        page = (skip // limit) + 1 if limit > 0 else 1
        total_pages = (total + limit - 1) // limit if limit > 0 else 1
        has_next = page < total_pages
        has_prev = page > 1

        return PaginatedResponse(
            items=items,
            total=total,
            page=page,
            page_size=limit,
            total_pages=total_pages,
            has_next=has_next,
            has_prev=has_prev
        )

    @classmethod
    async def _find_paginated_with_relations(
            cls,
            query: Dict,
            skip: int = 0,
            limit: int = 100,
            sort: Optional[List[tuple]] = None,
    ) -> PaginatedResponse:
        """Пагинация с загрузкой связанных объектов через агрегацию"""
        # Получаем общее количество документов
        total = await cls.collection.count_documents(query)

        # Строим пайплайн агрегации
        pipeline = [{"$match": query}]

        # Добавляем сортировку
        if sort:
            pipeline.append({"$sort": dict(sort)})

        # Добавляем пагинацию
        pipeline.extend([
            {"$skip": skip},
            {"$limit": limit}
        ])

        # Добавляем lookup'ы для связанных объектов
        pipeline.extend(cls._get_relation_lookups())

        # Выполняем агрегацию
        items = await cls.aggregate(pipeline)

        # Конвертируем ObjectId в строки
        items = cls._convert_objectids_to_str(items)

        # Вычисляем метаданные пагинации
        page = (skip // limit) + 1 if limit > 0 else 1
        total_pages = (total + limit - 1) // limit if limit > 0 else 1
        has_next = page < total_pages
        has_prev = page > 1

        return PaginatedResponse(
            items=items,
            total=total,
            page=page,
            page_size=limit,
            total_pages=total_pages,
            has_next=has_next,
            has_prev=has_prev
        )

    @classmethod
    def _get_relation_lookups(cls) -> List[Dict]:
        """Возвращает список lookup'ов для связанных объектов"""
        return [
            {
                "$lookup": {
                    "from": "services",
                    "localField": "serviceId",
                    "foreignField": "_id",
                    "as": "service"
                }
            },
            {
                "$lookup": {
                    "from": "customers",
                    "localField": "customerId",
                    "foreignField": "_id",
                    "as": "customer"
                }
            },
            {
                "$lookup": {
                    "from": "stages",
                    "localField": "stageId",
                    "foreignField": "_id",
                    "as": "stage"
                }
            },
            {
                "$lookup": {
                    "from": "materials",
                    "localField": "materialId",
                    "foreignField": "_id",
                    "as": "material"
                }
            },
            {
                "$lookup": {
                    "from": "addresses",
                    "localField": "shippingAddressId",
                    "foreignField": "_id",
                    "as": "shipping_address"
                }
            },
            {
                "$lookup": {
                    "from": "addresses",
                    "localField": "deliveryAddressId",
                    "foreignField": "_id",
                    "as": "delivery_address"
                }
            },
            {
                "$lookup": {
                    "from": "users",
                    "localField": "userId",
                    "foreignField": "_id",
                    "as": "user"
                }
            },
            {
                "$addFields": {
                    "service": {"$arrayElemAt": ["$service", 0]},
                    "customer": {"$arrayElemAt": ["$customer", 0]},
                    "stage": {"$arrayElemAt": ["$stage", 0]},
                    "material": {"$arrayElemAt": ["$material", 0]},
                    "shipping_address": {"$arrayElemAt": ["$shipping_address", 0]},
                    "delivery_address": {"$arrayElemAt": ["$delivery_address", 0]},
                    "user": {"$arrayElemAt": ["$user", 0]},
                }
            }
        ]

    @classmethod
    def _convert_objectids_to_str(cls, data: Any) -> Any:
        """Рекурсивно конвертирует ObjectId в строки"""
        if isinstance(data, ObjectId):
            return str(data)
        elif isinstance(data, dict):
            result = {}
            for key, value in data.items():
                # Специальная обработка для unitMeasurement
                if key == "unitMeasurement" and (value == "" or value is None):
                    result[key] = None
                else:
                    result[key] = cls._convert_objectids_to_str(value)
            return result
        elif isinstance(data, list):
            return [cls._convert_objectids_to_str(item) for item in data]
        else:
            return data
