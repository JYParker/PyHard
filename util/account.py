from pymongo import MongoClient
import bcrypt
import models.user_model


#비밀번호 해싱 후 저장
def hashing(pw):
    hashed = bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()
    return hashed

# 로그인 시 비밀번호 체크
def pw_check(pw, hashed):
    return bcrypt.checkpw(pw.encode(), hashed.encode())

# 아이디가 이미 있는 아이디인지 체크
def check_double_regist(id):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['user_db']
    collection = db['users']

    if collection.count_documents({}) == 0:
        return False  # 컬렉션이 비어있으면 무조건 가입 가능
    else:
        user = collection.find_one({'id':id})
        return user is not None

#로그인 함수
def sign_in(info_list):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['user_db']
    collection = db['users']

    id = info_list[0]
    pw = info_list[1]

    user = collection.find_one({"id": id})

    if pw_check(id, user['pw']) and user:
        return id
    else:
        False

#회원가입함수
def sign_up(info_list):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['user_db']
    collection = db['users']

    user ={
    "name" : info_list[0],
    "email" : info_list[1],
    "id" : info_list[2],
    "pw" : hashing(info_list[3])
    }

    double_check = check_double_regist(info_list[2])    #이미 존재하는 아이디인지 체크
    if double_check:
        return [False, "이미 존재하는 아이디입니다."]
    else:
        try:
            collection.insert_one(user)
            return True
        except:
            return [False,"오류가 발생하였습니다. 다시 시도해주세요"]  # 오류 발생 체크
