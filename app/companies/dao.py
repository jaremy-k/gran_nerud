from app.dao.base import MongoDAO
from app.database import database_mongo


class CompaniesDAO(MongoDAO):
    collection = database_mongo["companies"]
