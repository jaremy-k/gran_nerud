from app.dao.base import MongoDAO
from app.database import database_mongo


class DealsDAO(MongoDAO):
    collection = database_mongo["deals"]
