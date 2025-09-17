from flask import Flask, render_template, request

dummy_files = [
    {
        'id': 'file123',
        'title': '2024년_프로젝트_계획서.xlsx',
        'size': '1.2 MB',
        'document_name': '2024년_프로젝트_계획서.xlsx',
        'uploader_name': '김서연'
    },
    {
        'id': 'file456',
        'title': '웹하드_GUI_디자인.png',
        'size': '5.8 MB',
        'document_name': '웹하드_GUI_디자인.png',
        'uploader_name': '박지훈'
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

@app.route("/")
def index():
    return render_template('main.html', files=dummy_files)

if __name__ == '__main__':
    app.run(debug=True)

