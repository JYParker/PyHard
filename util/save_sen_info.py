import os
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["webhard"]
files_collection = db["files"]

def save_result(user_id, file_path, result):
    ext = os.path.splitext(file_path)[1].lower()

    files_collection.insert_one({
        "user_id": user_id,
        "filename": os.path.basename(file_path),
        "extension": ext,
        "sensitive_info": result
    })
