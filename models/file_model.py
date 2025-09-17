# 파일 정보
from models.db import get_collection
from datetime import datetime

def save_file_info(filename, uploader, sensitive, path):
    files = get_collection("files")
    files.insert_one({
        "filename": filename,
        "uploader": uploader,
        "upload_time": datetime.now(),
        "sensitive": sensitive,
        "path": path
    })

def get_file(filename):
    files = get_collection("files")
    return files.find_one({"filename": filename})