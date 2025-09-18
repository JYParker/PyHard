import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from pymongo import MongoClient
import os
import shutil
from dotenv import load_dotenv

# 이메일 보내기
def mail_sender(report_file, recv_id):

    client = MongoClient("mongodb://localhost:27017/")
    db = client["webhard_project"]
    collection = db["users"]

    load_dotenv()

    send_email = os.getenv("SECRET_ID")
    send_pwd = os.getenv("SECRET_PASS")

    smtp = smtplib.SMTP('smtp.naver.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(send_email, send_pwd)

    recv_email = collection.find_one({'username':recv_id})['email']
    msg = MIMEMultipart()
    msg['Subject'] = f"민감정보 식별 결과 안내"
    msg['From'] = send_email
    msg['To'] = recv_email

    text = f"업로드하신 파일에서 개인정보가 탐지되었습니다."
    msg.attach(MIMEText(text))
    print(report_file)
    with open(report_file, 'rb') as file:
        part = MIMEApplication(file.read())
        part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(report_file))
        msg.attach(part)

    smtp.sendmail(send_email, recv_email, msg.as_string())
    smtp.quit()


# DB에서 민감정보 가져오기
def load_data():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["webhard"]
    collection = db["files"]

    results = collection.find()
    local_files = []

    for doc in results:
        user_email = doc.get("user_id")
        filename = doc.get("filename")

        # 원본 파일 경로: uploads 폴더에서 찾기
        original_path = os.path.join("./uploads", filename)
        if not os.path.exists(original_path):
            print(f"파일 {filename}을 찾을 수 없습니다.")
            continue

        # 로컬 저장 폴더
        local_dir = "./sensitive_files"
        os.makedirs(local_dir, exist_ok=True)
        local_file_path = os.path.join(local_dir, filename)

        shutil.copy(original_path, local_file_path)
        local_files.append({"user_email": user_email, "local_file": local_file_path})

    return local_files


# # 메인 실행
# if __name__ == "__main__":
#     files_info = load_data()

#     for item in files_info:
#         mail_sender(item["local_file"], item["user_email"])
