from flask import Flask, render_template,request
from flask import redirect, url_for, session
from util import account
from models.config import SECRET_KEY

dummy_files = [
    {
        'id': 'file123',
        'title': '2024년_프로젝트_계획서.xlsx',
        'size': '1.2 MB',
        'document_name': '2024년_프로젝트_계획서.xlsx',
        'uploader_name': '김서연'
    },
    {
        'id': 'file789',
        'title': '팀_회의록_20240315.txt',
        'size': '25 KB',
        'document_name': '팀_회의록_20240315.txt',
        'uploader_name': '이준호'
    },
    {
        'id': 'file101',
        'title': '민감정보_테스트_자료.zip',
        'size': '3.4 MB',
        'document_name': '민감정보_테스트_자료.zip',
        'uploader_name': '최유리'
    }
]

app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.route("/")
def index():
    ## 세션에 'user_id' 있는지 확인해서 로그인 상태 파악
    is_logged_in = 'user_id' in session
    # is_logged_in 변수와 dummy_files 전달
    return render_template('main.html', files=dummy_files, is_logged_in=is_logged_in)

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

if __name__ == '__main__':
    app.run(debug=True)

