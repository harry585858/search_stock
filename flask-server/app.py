from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import hashlib
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, func
import os
import requests
#https://github.com/harry585858/search_stock.git
app = Flask(__name__)

#내부 데이터베이스 URI 설정 (현재 디렉토리에 example.db 파일 생성)
basedir = os.path.abspath(os.path.dirname(__file__))  # 현재 파일의 디렉토리 경로
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "example.db")}'
app.config['SECRET_KEY'] = 'password'

# 외부 데이터베이스 설정
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:비번%21@database-1.c5cys28ymsiz.ap-northeast-2.rds.amazonaws.com:3306/test'

#config
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 데이터베이스 모델 정의
class User(db.Model):
    __tablename__ = 'user_data'
    id = db.Column(db.String(50), primary_key=True)
    pw = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    favorites = db.relationship('FavoriteItem', backref='user', lazy=True)
    rate = db.relationship('rateItem', backref='user', lazy=True)
    def __repr__(self):
        return f'<User {self.id}>'

class FavoriteItem(db.Model):
    __tablename__ = 'Userfavorite'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), db.ForeignKey('user_data.id'), nullable=False)
    item_id = db.Column(db.String(50), nullable=False)  # 즐겨찾기 항목 ID
class rateItem(db.Model):
    __tablename__ = 'Userrating'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), db.ForeignKey('user_data.id'), nullable=False)
    item_id = db.Column(db.String(50), nullable=False)  # 즐겨찾기 항목 ID
    star = db.Column(db.Integer,nullable=False)
    rate = db.Column(db.String(500),nullable=False)

with app.app_context():
    db.create_all()

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
    token_url = f"{Config.NAVER_TOKEN_URL}?grant_type=authorization_code&client_id={Config.NAVER_CLIENT_ID}&client_secret={Config.NAVER_CLIENT_SECRET}&code={code}&state={state}"
    token_response = requests.get(token_url)
    token_data = token_response.json()
    access_token = token_data.get('access_token')
    headers = {'Authorization': f'Bearer {access_token}'}
    profile_response = requests.get(Config.NAVER_PROFILE_URL, headers=headers)
    profile_data = profile_response.json()
    if profile_data.get('response'):
        user_info = profile_data['response']
        return jsonify(user_info)
    else:
        return jsonify({"error": "Failed to retrieve user info"}), 400

@app.route('/search', methods=['POST'])
def search():
    nameOfStock = request.form.getlist('nameOfStock[]')
    return render_template('search.html', nameOfStock=nameOfStock)

@app.route('/makeresult', methods=['POST'])
def makeresult():
    salt = 'HZaNK0en1n'
    id = request.form['id']
    pw = request.form['pw']
    email = request.form['email']
    if not id or not pw or not email:
        return render_template('makeresult.html', result=False, error=1)
    pw = hashlib.sha512((pw + salt).encode()).hexdigest()
    existing_user = User.query.filter_by(id=id).first()
    if existing_user:
        return render_template('makeresult.html', result=False, error=0)
    new_user = User(id=id, pw=pw, email=email)
    db.session.add(new_user)
    db.session.commit()
    return render_template('makeresult.html', result=True)

@app.route('/signup/check', methods=['POST'])
def signup_check():
    id = request.form['id']
    email = request.form['email']
    existing_user = User.query.filter_by(id=id).first()
    existing_email = User.query.filter_by(email=email).first()
    if existing_user or existing_email:
        if existing_email:
            return jsonify({"error": "same_email"})
        if existing_user:
            return jsonify({"error": "same_user"})
    return jsonify({"success": "0"})

@app.route('/stockdetail', methods=['POST'])
def stockdetail():
    stockname = request.form("stockname", none)
    user_id = session.get('user_id')
    existing_favorite = FavoriteItem.query.filter_by(user_id=user_id, item_id=stockname).first()
    star = db.session.query(func.avg(rateItem.star)).filter(rateItem.item_id==stockname).scalar()
    if star:
        return jsonify({"평균평점": star, "즐겨찾기 여부": existing_favorite})
    else:
        return jsonify({"error", "존재안함"})

@app.route('/stockdetail/favorite/<string:item_id>', methods=['POST', 'DELETE'])
def stockdetail_favorite(item_id):
    user_id = session.get('user_id')  # 세션에서 사용자 ID 가져오기
    
    if request.method == 'POST':
        # 즐겨찾기 추가
        existing_favorite = FavoriteItem.query.filter_by(user_id=user_id, item_id=item_id).first()
        if existing_favorite:
            return jsonify({"message": f"Item {item_id} is already in favorites"}), 200
        
        new_favorite = FavoriteItem(user_id=user_id, item_id=item_id)
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify({"message": f"Item {item_id} added to favorites"}), 201

    elif request.method == 'DELETE':
        # 즐겨찾기 삭제
        favorite = FavoriteItem.query.filter_by(user_id=user_id, item_id=item_id).first()
        if favorite:
            db.session.delete(favorite)
            db.session.commit()
            return jsonify({"message": f"Item {item_id} removed from favorites"}), 200
        else:
            return jsonify({"error": "Favorite not found"}), 404

@app.route('/stockdetail/rate/<string:item_id>', methods=['POST'])
def stockdetail_rate(item_id):
    user_id = session.get('user_id')
    star = request.form("star")
    rate = request.form("rate")
    existing_rate = FavoriteItem.query.filter_by(user_id=user_id, item_id=item_id).first()
    if existing_rate:
        new_rate = rateItem(id=id, user_id=user_id,item_id=item_id, star=star,rate=rate)
        db.session.add(new_rate)
        db.session.commit()
        return jsonify({"message": "저장 완료"})
    else:return jsonify({"message": "이미 존재"})
        

@app.route('/stockdetail/ratedelete/<string:item_id>', methods=['DELETE'])
def stockdetail_ratedelete():
    user_id = session.get('user_id')
    existing_rate = FavoriteItem.query.filter_by(user_id=user_id, item_id=item_id).first()
    if existing_rate:
        db.session.delete(existing_rate)
        db.session.commit()
        return jsonify({"message": "Rate delete"})
    else:
        return jsonify({"message": "없음"}), 404

@app.route('/makelogin', methods=['POST'])
def makelogin():
    salt = 'HZaNK0en1n'
    id = request.form['id']
    pw = request.form['pw']
    if not id or not pw:
        return render_template('makelogin.html', success=False)
    pw = hashlib.sha512((pw + salt).encode()).hexdigest()
    user = User.query.filter_by(id=id, pw=pw).first()
    if user:
        session['user_id'] = id
        session['logged_in'] = True
        return render_template('makelogin.html', success=True)
    else:
        return render_template('makelogin.html', success=False)
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('logged_in', None)
    return redirect(url_for('login'))
@app.route('/mypage', methods=['POST'])
def mypage():
    user_id = session.get('user_id')
    favoriteList = FavoriteItem.query.filter_by(user_id=user_id).all()
    if favoriteList:
        return jsonify({"message": "Item in favorites"}), 200
    else:
        return jsonify({"message": "nothing"}), 200
#####
@app.route('/')
def index():
    if 'logged_in' in session and session['logged_in']:
        user = User.query.get(session.get('user_id'))
        favorites = user.favorites
        return render_template('index.html', logined = True, favorites=favorites)

    else:
        return render_template('index.html', logined = False)
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/makeid')
def makeid():
    return render_template('makeid.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)