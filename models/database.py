import pymongo as mongoDB
from config import ROOMMATES_DB_LINK


db_handler = mongoDB.MongoClient(ROOMMATES_DB_LINK)
db = db_handler.main

Roommate = db.Roommate