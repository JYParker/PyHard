# 회원 정보
from models.db import get_collection
from datetime import datetime

def create_user(name,  email, username, password):
    users = get_collection("users")
    users.insert_one({
        "name" : name ,
        "username": username,
        "password": password,
        "email": email,
        "created_at": datetime.now()
    })

def find_user(username):
    users = get_collection("users")
    return users.find_one({"username": username})