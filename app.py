from flask import Flask, render_template, send_from_directory, request
from flask import redirect, url_for, session
from util import account
from models.config import SECRET_KEY
import os
from datetime import datetime
from pymongo import MongoClient 
from werkzeug.utils import secure_filename
from util import warning_mail1
import util.scan as scan

app = Flask(__name__)
app.secret_key = SECRET_KEY

# MongoDB 연결
client = MongoClient("mongodb://localhost:27017/")
db = client["webhard_project"]
files_collection = db["files"]

# 업로드 폴더 지정
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# 업로드 허용 확장자
ALLOWED_EXTENSIONS = {"txt", "xlsx", "xls", "zip"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    # 로그인 체크
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    # DB에서 파일 조회
    files = list(files_collection.find({"uploader":session["user_id"]}, {"_id": 0}))
    ## 세션에 'user_id' 있는지 확인해서 로그인 상태 파악
    is_logged_in = 'user_id' in session
    return render_template('main.html', files=files, is_logged_in=is_logged_in)

#    # is_logged_in 변수와 dummy_files 전달
#    return render_template('main.html', files=dummy_files, is_logged_in=is_logged_in)

@app.route("/intro")
def intro():
    return render_template("intro.html")

# 로그인 페이지 렌더링
@app.route('/login')
def login_page():
    return render_template('login.html')

# 로그인 처리
@app.route('/login', methods=['POST'])
def login_post():
    info_list = [request.form['id'], request.form['password']]
    
    result = account.sign_in(info_list)
    
    if result:
        # 로그인 성공. sign_in 함수에서 id 반환
        session['user_id'] = result
        return redirect(url_for('index'))
    else:
        # 로그인 실패. sign_in 함수에서 False 반환
        return render_template('login.html', error_message='아이디 또는 비밀번호가 올바르지 않습니다.')

# 회원가입 페이지 렌더링
@app.route('/register')
def register_page():
    return render_template('register.html')

# 회원가입 처리
@app.route('/register', methods=['POST'])
def register_post():
    info_list = [
        request.form['name'],
        request.form['email'],
        request.form['id'],
        request.form['password']
    ]
    
    result = account.sign_up(info_list)
    
    if result is True:
        # 회원가입 성공.
        return redirect(url_for('login_page'))
    else:
        # 회원가입 실패. sign_up 함수에서 [False, 메시지] 반환
        return render_template('register.html', error_message=result[1])

# 로그아웃 기능
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

# 파일 업로드 페이지 렌더링
@app.route("/upload_page")
def upload_page():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    # 업로드된 파일 목록 불러오기 (account.py의 로직이 없으므로 직접 가져옴)
    files = list(files_collection.find({}, {"_id": 0}))
    
    # 로그인 상태 확인 변수도 함께 전달 (헤더를 위해)
    is_logged_in = 'user_id' in session
    return render_template("upload.html", files=files, is_logged_in=is_logged_in)


# 파일 업로드
@app.route("/upload", methods=["POST"])
def upload_file():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    if request.method == "POST":
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        if "file" not in request.files:
            return "파일이 없습니다!", 400
        
        file = request.files["file"]

        if file.filename == "":
            return "선택된 파일이 없습니다!", 400
        
        if file and allowed_file(file.filename):
            file_sen=False
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            if scan.scan_file(filepath):
                print(type(session['user_id']))
                warning_mail1.mail_sender(filepath,session['user_id'])
                file_sen=True

            # MongoDB에 메타데이터 저장
            metadata = {
                "filename": filename,
                "uploader": session['user_id'],
                "upload_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "sensitive": file_sen,
                "path": filepath
            }
            files_collection.insert_one(metadata)

            return redirect(url_for("upload_page"))
        return "허용되지 않는 파일 확장자입니다.", 400
# 파일 다운로드
@app.route("/download/<filename>")
def download_file(filename):
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)

@app.route("/delete/<filename>", methods=["POST"])
def delete_file(filename):
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    # 서버 폴더에서 파일 삭제
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    
    # MongoDB에서 삭제
    files_collection.delete_one({"filename": filename})
    
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)

