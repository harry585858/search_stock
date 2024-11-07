from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import hashlib
from flask_sqlalchemy import SQLAlchemy
import os
import requests

# Flask 애플리케이션 초기화
app = Flask(__name__)

#내부 데이터베이스 URI 설정 (현재 디렉토리에 example.db 파일 생성)
#basedir = os.path.abspath(os.path.dirname(__file__))  # 현재 파일의 디렉토리 경로
#f'sqlite:///{os.path.join(basedir, "example.db")}'
#app.config['SECRET_KEY'] = 'password'

#외부db설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:비번%21@database-1.c5cys28ymsiz.ap-northeast-2.rds.amazonaws.com:3306/test'

#config
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemy 객체 생성 및 초기화
db = SQLAlchemy(app)

# 데이터베이스 모델 정의
class User(db.Model):
    __tablename__ = 'user_data'
    id = db.Column(db.String(50), primary_key=True)
    pw = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.id}>'

# 데이터베이스 초기화 및 테이블 생성
with app.app_context():
    db.create_all()  # 데이터베이스가 없다면 생성합니다.

# 네이버 로그인 요청
@app.route('/naver/login')
def naver_login():
    naver_auth_url = f"{Config.NAVER_AUTH_URL}?response_type=code&client_id={Config.NAVER_CLIENT_ID}&redirect_uri={Config.NAVER_REDIRECT_URI}&state=RANDOM_STATE"
    return redirect(naver_auth_url)

# 네이버 로그인 콜백
@app.route('/naver/callback')
def naver_callback():
    code = request.args.get('code')
    state = request.args.get('state')
    
    # 액세스 토큰 요청
    token_url = f"{Config.NAVER_TOKEN_URL}?grant_type=authorization_code&client_id={Config.NAVER_CLIENT_ID}&client_secret={Config.NAVER_CLIENT_SECRET}&code={code}&state={state}"
    token_response = requests.get(token_url)
    token_data = token_response.json()
    access_token = token_data.get('access_token')
    
    # 프로필 정보 요청
    headers = {'Authorization': f'Bearer {access_token}'}
    profile_response = requests.get(Config.NAVER_PROFILE_URL, headers=headers)
    profile_data = profile_response.json()
    
    if profile_data.get('response'):
        user_info = profile_data['response']
        return jsonify(user_info)
    else:
        return jsonify({"error": "Failed to retrieve user info"}), 400

# @app.route('/')
# def index():
#     if 'logged_in' in session and session['logged_in']:
#         return render_template('index.html', logined=True)
#     else:
#         return render_template('index.html', logined=False)

# @app.route('/login')
# def login():
#     return render_template('login.html')

@app.route('/search', methods=['POST'])
def search():
    nameOfStock = request.form.getlist('nameOfStock[]')
    return render_template('search.html', nameOfStock=nameOfStock)

# @app.route('/makeid')
# def makeid():
#     return render_template('makeid.html')

@app.route('/makeresult', methods=['POST'])
def makeresult():
    salt = 'HZaNK0en1n'
    id = request.form['id']
    pw = request.form['pw']
    email = request.form['email']
    if not id or not pw or not email:
        return render_template('makeresult.html', result=False, error=1)  # 빈공간 있음
    
    # 비밀번호 해싱
    pw = hashlib.sha512((pw + salt).encode()).hexdigest()

    # SQLAlchemy 사용하여 데이터베이스에 저장
    existing_user = User.query.filter_by(id=id).first()
    if existing_user:
        return render_template('makeresult.html', result=False, error=0)  # id 중복
    else:
        new_user = User(id=id, pw=pw, email=email)
        db.session.add(new_user)
        db.session.commit()
        return render_template('makeresult.html', result=True)
@app.route('/signup/check',methods['POST'])
def signup_check():
    id = request.form['id']
    pw = request.form['pw']
    email = request.form['email']
    existing_user = User.query.filter_by(id=id).first()
    existing_email = User.quert.filter_by(email=email).first()
    if existing_user and existing_email:
        return jsonify({"error": "1"})

@app.route('searchstock')
def searchstock():

@app.route('stockdetail')
def stockdetail():

@app.route('stockdetail/fatorite')
def stockdetail_favorite():
@app.route('stockdetail/rate')
def stockdetail_rate():
    @app.route('stockdetail/ratedelete')
def stockdetail_ratedelete():


@app.route('/makelogin', methods=['POST'])
def makelogin():
    salt = 'HZaNK0en1n'
    id = request.form['id']
    pw = request.form['pw']
    if not id or not pw:
        return render_template('makelogin.html', success=False)  # 빈공간 있음
    
    # 비밀번호 해싱
    pw = hashlib.sha512((pw + salt).encode()).hexdigest()

    # SQLAlchemy를 사용하여 데이터베이스에서 사용자 조회
    user = User.query.filter_by(id=id, pw=pw).first()
    if user:
        session['user_id'] = id
        session['logged_in'] = True
        return render_template('makelogin.html', success=True)
    else:
        return render_template('makelogin.html', success=False)  # 로그인 실패

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=8000)