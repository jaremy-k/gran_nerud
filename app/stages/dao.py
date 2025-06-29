from app.dao.base import MongoDAO
from app.database import database_mongo


class StagesDAO(MongoDAO):
    collection = database_mongo["stages"]
