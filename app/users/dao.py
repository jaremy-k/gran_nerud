from app.dao.base import MongoDAO
from app.database import database_mongo


class UsersDAO(MongoDAO):
    collection = database_mongo["users"]
