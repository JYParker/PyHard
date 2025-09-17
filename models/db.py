from pymongo import MongoClient
import config

client = MongoClient('mongodb://localhost:27017/')
db = client['member_management']
collection = db['members']

def init_db():
    global client, db
    client = MongoClient(config.MONGO_URI)
    db = client[config.DB_NAME]

def get_collection(name):
    return db[name]