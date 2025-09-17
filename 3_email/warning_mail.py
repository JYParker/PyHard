import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication 
from dotenv import load_dotenv
import os 
import shutil

from pymongo import MongoClient

# 이메일 보내기
def mail_sender(refort_file, recv_email):
    load_dotenv()

    # 보내는 사람 이메일 + .env 파일에 작성해 주셔야합니다.
    send_email = os.getenv("SECRET_ID")
    send_pwd = os.getenv("SECRET_PASS")

    smtp = smtplib.SMTP('smtp.naver.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(send_email, send_pwd)

    msg = MIMEMultipart()
    msg['Subject'] = f"민감정보가 식별되어 알려드립니다."  
    msg['From'] = send_email          
    msg['To'] = recv_email

    text = f"민감정보 식별결과는 참조파일을 확인하여 주시길 바랍니다"

    contentPart = MIMEText(text)
    msg.attach(contentPart)

    etc_file_path = refort_file
    with open(etc_file_path, 'rb') as file:
        etc_part = MIMEApplication(file.read())
        etc_part.add_header('Content-Disposition', 'attachment', filename=etc_file_path)
        msg.attach(etc_part)

    smtp.sendmail(send_email, recv_email, msg.as_string())
    smtp.quit()


# DB 에서 민감정보 파일 가져오기 + 사용자 email
def load_data():
    client = MongoClient('mongodb://localhost:27017')
    db = client['user_db'] 
    collection = db['users'] 

    results = collection.find()

    local_files = []

    for doc in results:
        user_email = doc.get("email")
        filename = doc.get("filename")
        file_path = doc.get("file_path")

        # 로컬 저장 경로
        local_dir = "./sensitive_files"
        os.makedirs(local_dir, exist_ok=True)
        local_file_path = os.path.join(local_dir, filename)

        # 서버 파일을 내 로컬로 복사
        shutil.copy(file_path, local_file_path)

        local_files.append({"user_email": user_email, "local_file": local_file_path})

    return local_files

# 메인
if __name__ == "__main__":
    files_info = load_data()  # DB에서 파일 가져와서 로컬에 저장

    for item in files_info:
        mail_sender(item["local_file"], item["user_email"])
