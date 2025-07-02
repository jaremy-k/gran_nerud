from typing import Optional, Dict, List

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import BaseModel
# from sqlalchemy.exc import SQLAlchemyError
# from app.database import async_session_maker
# from sqlalchemy import select, insert, delete, update

from app.logger import logger


# class BaseDAO:
#     model = None
#
#     @classmethod
#     async def find_one_or_none(cls, **data):
#         async with async_session_maker() as session:
#             query = select(cls.model).filter_by(**data)
#             result = await session.execute(query)
#             return result.scalars().one_or_none()
#
#     @classmethod
#     async def find_all(cls, **data):
#         async with async_session_maker() as session:
#             query = select(cls.model).filter_by(**data)
#             result = await session.execute(query)
#             return result.scalars().all()
#
#     @classmethod
#     async def add(cls, **data):
#         msg = ''
#         try:
#             query = insert(cls.model).values(**data).returning(cls.model)
#             async with async_session_maker() as session:
#                 result = await session.execute(query)
#                 await session.commit()
#                 return result.mappings().first()
#         except (SQLAlchemyError, Exception) as e:
#             if isinstance(e, SQLAlchemyError):
#                 msg = "Database Exc"
#             elif isinstance(e, Exception):
#                 msg = "Unknown Exc"
#             msg += ": Cannot insert data into table"
#             logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
#             return None
#
#     @classmethod
#     async def update_by_id(cls, object_id: int, data):
#         async with async_session_maker() as session:
#             query = update(cls.model).where(cls.model.id == object_id).values(**data).returning(cls.model)
#             result = await session.execute(query)
#             await session.commit()
#             return result
#
#     @classmethod
#     async def update(cls, phone_number, **data):
#         async with async_session_maker() as session:
#             query = update(cls.model).where(cls.model.phone_number == phone_number).values(**data).returning(cls.model)
#             result = await session.execute(query)
#             await session.commit()
#             return result
#
#     @classmethod
#     async def delete(cls, **data):
#         async with async_session_maker() as session:
#             query = delete(cls.model).filter_by(**data)
#             await session.execute(query)
#             await session.commit()
#
#     @classmethod
#     async def add_bulk(cls, *data):
#         # Для загрузки массива данных [1, 2]
#         # мы должны обрабатывать его через позиционные аргументы *args.
#         msg = ''
#         try:
#             query = insert(cls.model).values(*data).returning(cls.model.id)
#             async with async_session_maker() as session:
#                 result = await session.execute(query)
#                 await session.commit()
#                 return result.mappings().first()
#         except (SQLAlchemyError, Exception) as e:
#             if isinstance(e, SQLAlchemyError):
#                 msg = "Database Exc"
#             elif isinstance(e, Exception):
#                 msg = "Unknown Exc"
#             msg += ": Cannot insert data into table"
#             extra = {"table": cls.model.__tablename__}
#             logger.error(msg, extra={extra}, exc_info=True)
#             return None


class MongoDAO:
    collection: AsyncIOMotorCollection = None

    @classmethod
    async def find_one_or_none(cls, **filter_by) -> Optional[BaseModel]:
        try:
            document = await cls.collection.find_one(filter_by)
            return document if document else None
        except Exception as e:
            logger.error(f"Error finding document: {str(e)}", exc_info=True)
            return None

    @classmethod
    async def find_all(
            cls,
            *,
            filter_by: Optional[Dict] = None,
            skip: int = 0,
            limit: int = 100,
            sort: Optional[List[tuple]] = None
    ) -> List[BaseModel]:
        try:
            filter_by = filter_by or {}
            cursor = cls.collection.find(filter_by)

            if sort:
                cursor = cursor.sort(sort)

            cursor = cursor.skip(skip).limit(limit)

            return [doc async for doc in cursor]
        except Exception as e:
            logger.error(f"Error finding documents: {str(e)}", exc_info=True)
            return []

    @classmethod
    async def add(cls, **data) -> Optional[BaseModel]:
        try:
            result = await cls.collection.insert_one(data)
            if result.inserted_id:
                document = await cls.collection.find_one({"_id": result.inserted_id})
                return cls.collection(**document)
            return None
        except Exception as e:
            logger.error(f"Error inserting document: {str(e)}", exc_info=True)
            return None

    @classmethod
    async def update_by_id(
            cls,
            object_id: str,
            **update_data
    ) -> Optional[BaseModel]:
        try:
            result = await cls.collection.update_one(
                {"_id": ObjectId(object_id)},
                {"$set": update_data}
            )
            if result.modified_count:
                document = await cls.collection.find_one({"_id": ObjectId(object_id)})
                return cls.collection(**document)
            return None
        except Exception as e:
            logger.error(f"Error updating document: {str(e)}", exc_info=True)
            return None

    @classmethod
    async def update(
            cls,
            filter_by: Dict,
            **update_data
    ) -> Optional[BaseModel]:
        try:
            result = await cls.collection.update_one(
                filter_by,
                {"$set": update_data}
            )
            if result.modified_count:
                document = await cls.collection.find_one(filter_by)
                return cls.collection(**document)
            return None
        except Exception as e:
            logger.error(f"Error updating document: {str(e)}", exc_info=True)
            return None

    @classmethod
    async def delete(cls, **filter_by) -> bool:
        try:
            result = await cls.collection.delete_one(filter_by)
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting document: {str(e)}", exc_info=True)
            return False

    @classmethod
    async def add_bulk(cls, documents: List[Dict]) -> Optional[List[str]]:
        try:
            result = await cls.collection.insert_many(documents)
            return [str(id) for id in result.inserted_ids]
        except Exception as e:
            logger.error(f"Error bulk inserting documents: {str(e)}", exc_info=True)
            return None

    @classmethod
    async def count(cls, filter_by: Optional[Dict] = None) -> int:
        try:
            filter_by = filter_by or {}
            return await cls.collection.count_documents(filter_by)
        except Exception as e:
            logger.error(f"Error counting documents: {str(e)}", exc_info=True)
            return 0
