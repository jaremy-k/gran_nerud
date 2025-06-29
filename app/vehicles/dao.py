from app.dao.base import MongoDAO
from app.database import database_mongo


class VehiclesDAO(MongoDAO):
    collection = database_mongo["vehicles"]
