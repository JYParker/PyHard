from pymongo import MongoClient
from . import config

client = None
db = None

def init_db():
    global client, db
    client = MongoClient(config.MONGO_URI)
    db = client[config.DB_NAME]

def get_collection(name):
    return db[name]