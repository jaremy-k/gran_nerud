from app.dao.base import MongoDAO
from app.database import database_mongo


class ServicesDAO(MongoDAO):
    collection = database_mongo["services"]
