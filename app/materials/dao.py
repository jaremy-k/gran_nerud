from app.dao.base import MongoDAO
from app.database import database_mongo


class MaterialsDAO(MongoDAO):
    collection = database_mongo["materials"]
