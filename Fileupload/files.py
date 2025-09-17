from flask import Flask, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
from datetime import datetime
from pymongo import MongoClient
import os

app = Flask(__name__)

# 업로드 폴더 지정
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# MongoDB 연결
client = MongoClient("mongodb://localhost:27017/")
db = client["webhard"]
files_collection = db["files"]

# 업로드 허용 확장자
ALLOWED_EXTENSIONS = {"txt", "xlsx", "xls", "zip"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# 파일 업로드
@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "파일이 없습니다!", 400
        file = request.files["file"]
        if file.filename == "":
            return "선택된 파일이 없습니다!", 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            # MongoDB에 메타데이터 저장
            metadata = {
                "filename": filename,
                "uploader": request.remote_addr,  # 여기서는 IP로 업로더 표시
                "upload_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "path": filepath
            }
            files_collection.insert_one(metadata)

            return redirect(url_for("upload_file"))

    # 업로드된 파일 목록 불러오기
    files = list(files_collection.find({}, {"_id": 0}))
    return render_template("upload.html", files=files)

# 파일 다운로드
@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)

@app.route("/delete/<filename>", methods=["POST"])
def delete_file(filename):
    # 서버 폴더에서 파일 삭제
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    
    # MongoDB에서 삭제
    files_collection.delete_one({"filename": filename})
    
    return redirect(url_for("upload_file"))

if __name__ == "__main__":
    app.run(debug=True)