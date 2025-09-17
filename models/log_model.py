# 로그 기록
from models.db import get_collection
from datetime import datetime

def log_action(action, user, target=None, extra=None):
    logs = get_collection("logs")
    logs.insert_one({
        "action": action,
        "user": user,
        "target": target,
        "time": datetime.now(),
        "extra": extra
    })