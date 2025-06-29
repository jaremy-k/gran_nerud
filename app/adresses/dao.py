from app.dao.base import MongoDAO
from app.database import database_mongo


class AdressesDAO(MongoDAO):
    collection = database_mongo["adresses"]
