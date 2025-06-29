from motor.motor_asyncio import AsyncIOMotorClient
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

# engine = create_async_engine(settings.DATABASE_URL)
# async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

client_mongo = AsyncIOMotorClient(settings.MONGO_URL)
database_mongo = client_mongo.jaremybase


class Base(DeclarativeBase):
    pass
