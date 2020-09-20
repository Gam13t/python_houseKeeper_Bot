import pymongo as mongoDB
from pprint import pprint
from config import DB_LINK

try:
    db_handler = mongoDB.MongoClient(DB_LINK)
    db = db_handler.main
    Roommate = db.Roommate
    serverStatusResult = db.command("serverStatus")
    pprint(serverStatusResult)
except:
    print("Error while connecting to database...")
