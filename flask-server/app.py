from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import hashlib
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, func, DECIMAL
import os
import requests
from config import Config
#https://github.com/harry585858/search_stock.git
app = Flask(__name__)
#내부 데이터베이스 URI 설정 (현재 디렉토리에 example.db 파일 생성)
# basedir = os.path.abspath(os.path.dirname(__file__))  # 현재 파일의 디렉토리 경로
# app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "example.db")}'
# app.config['SECRET_KEY'] = 'password'

# 외부 데이터베이스 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://back:back1234@database-1.c5cys28ymsiz.ap-northeast-2.rds.amazonaws.com:3306/stockDB'

#config
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key='비밀키'
# 데이터베이스 모델 정의
class User(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.String(50), primary_key=True)
    user_password = db.Column(db.String(128), nullable=False)
    user_email = db.Column(db.String(120), unique=True, nullable=False)
    favorites = db.relationship('FavoriteItem', backref='user', lazy=True)
    rate = db.relationship('rateItem', backref='user', lazy=True)
    def __repr__(self):
        return f'<User {self.id}>'

class FavoriteItem(db.Model):
    __tablename__ = 'Userfavorite'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), db.ForeignKey('Users.user_id'), nullable=False)
    stock_code = db.Column(db.String(20), nullable=False)  # 즐겨찾기 항목 ID
class rateItem(db.Model):
    __tablename__ = 'Userrating'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), db.ForeignKey('Users.user_id'), nullable=False)
    stock_code = db.Column(db.String(20), nullable=False)  # 즐겨찾기 항목 ID
    rating = db.Column(db.DECIMAL(precision=2,scale=1),nullable=False)
    content = db.Column(db.String(500),nullable=False)
class Predictstocks(db.Model):
    __tablename__='Predictstocks'
    id = db.Column(db.Integer, primary_key=True)
    stock_name = db.Column(db.String(20), nullable=False)
    stock_code = db.Column(db.String(20), nullable=False)
class Onedaypredict(db.Model):
    __tablename__='Onedaypredict'
    id = db.Column(db.Integer, primary_key=True)
    stock_code = db.Column(db.String(20),db.ForeignKey('Predictstocks.stock_code',name='oneday_code'))
    price30min =db.Column(db.DECIMAL(precision=10,scale=2))
    price60min =db.Column(db.DECIMAL(precision=10,scale=2))
    price90min =db.Column(db.DECIMAL(precision=10,scale=2))
    price120min =db.Column(db.DECIMAL(precision=10,scale=2))
    price150min =db.Column(db.DECIMAL(precision=10,scale=2))
    price180min =db.Column(db.DECIMAL(precision=10,scale=2))
    price210min =db.Column(db.DECIMAL(precision=10,scale=2))
    price240min =db.Column(db.DECIMAL(precision=10,scale=2))
    price270min =db.Column(db.DECIMAL(precision=10,scale=2))
    price300min =db.Column(db.DECIMAL(precision=10,scale=2))
    price330min =db.Column(db.DECIMAL(precision=10,scale=2))
    price360min =db.Column(db.DECIMAL(precision=10,scale=2))
    price390min =db.Column(db.DECIMAL(precision=10,scale=2))
    price420min =db.Column(db.DECIMAL(precision=10,scale=2))
class Oneweekpredict(db.Model):
    __tablename__='Oneweekpredict'
    id = db.Column(db.Integer, primary_key=True)
    stock_code = db.Column(db.String(20),db.ForeignKey('Predictstocks.stock_code',name='oneweek_code'))
    price1day =db.Column(db.DECIMAL(precision=10,scale=2))
    price2day =db.Column(db.DECIMAL(precision=10,scale=2))
    price3day =db.Column(db.DECIMAL(precision=10,scale=2))
    price4day =db.Column(db.DECIMAL(precision=10,scale=2))
    price5day =db.Column(db.DECIMAL(precision=10,scale=2))
    price6day =db.Column(db.DECIMAL(precision=10,scale=2))
    price7day =db.Column(db.DECIMAL(precision=10,scale=2))
class Onemonthpredict(db.Model):
    __tablename__='Onemonthpredict'
    id = db.Column(db.Integer, primary_key=True)
    stock_code = db.Column(db.String(20),db.ForeignKey('Predictstocks.stock_code',name='onemonth_code'))
    price3day =db.Column(db.DECIMAL(precision=10,scale=2))
    price6day =db.Column(db.DECIMAL(precision=10,scale=2))
    price9day =db.Column(db.DECIMAL(precision=10,scale=2))
    price12day =db.Column(db.DECIMAL(precision=10,scale=2))
    price15day =db.Column(db.DECIMAL(precision=10,scale=2))
    price18day =db.Column(db.DECIMAL(precision=10,scale=2))
    price21day =db.Column(db.DECIMAL(precision=10,scale=2))
    price24day =db.Column(db.DECIMAL(precision=10,scale=2))
    price27day =db.Column(db.DECIMAL(precision=10,scale=2))
    price30day =db.Column(db.DECIMAL(precision=10,scale=2))
  
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
    existing_user = User.query.filter_by(user_id=id).first()
    if existing_user:
        return render_template('makeresult.html', result=False, error=0)
    new_user = User(user_id=id, user_password=pw, user_email=email)
    db.session.add(new_user)
    db.session.commit()
    return render_template('makeresult.html', result=True)

@app.route('/signup/check', methods=['POST'])
def signup_check():
    id = request.form['id']
    email = request.form['email']
    existing_user = User.query.filter_by(user_id=id).first()
    existing_email = User.query.filter_by(user_email=email).first()
    if existing_user or existing_email:
        if existing_email:
            return jsonify({"error": "same_email"})
        if existing_user:
            return jsonify({"error": "same_user"})
    return jsonify({"success": "0"})

@app.route('/stockdetail', methods=['POST'])
def stockdetail():
    stock_code = request.form("stock_code", none)
    user_id = session.get('user_id')
    existing_favorite = FavoriteItem.query.filter_by(user_id=user_id, stock_code=stock_code).first()
    avg_rate = db.session.query(func.avg(rateItem.rating)).filter(rateItem.stock_code==stock_code).scalar()
    predict_day = Onedaypredict.query.filter_by(stock_code = stock_code).all()
    if avg_rate:
        return jsonify({"평균평점": avg_rate, "즐겨찾기 여부": existing_favorite, "예측데이터": predict_day})
    else:
        return jsonify({"error", "존재안함"})

@app.route('/stockdetail/favorite/<string:stock_code>', methods=['POST', 'DELETE'])
def stockdetail_favorite(stock_code):
    user_id = session.get('user_id')  # 세션에서 사용자 ID 가져오기
    
    if request.method == 'POST':
        # 즐겨찾기 추가
        existing_favorite = FavoriteItem.query.filter_by(user_id=user_id, stock_code=stock_code).first()
        if existing_favorite:
            return jsonify({"message": f"Item {stock_code} is already in favorites"}), 200
        
        new_favorite = FavoriteItem(user_id=user_id, stock_code=stock_code)
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify({"message": f"Item {stock_code} added to favorites"}), 201

    elif request.method == 'DELETE':
        # 즐겨찾기 삭제
        favorite = FavoriteItem.query.filter_by(user_id=user_id, stock_code=stock_code).first()
        if favorite:
            db.session.delete(favorite)
            db.session.commit()
            return jsonify({"message": f"Item {stock_code} removed from favorites"}), 200
        else:
            return jsonify({"error": "Favorite not found"}), 404

@app.route('/stockdetail/rate/<string:stock_code>', methods=['POST'])
def stockdetail_rate(stock_code):
    user_id = session.get('user_id')
    rating = request.form("rating")
    content = request.form("content")
    existing_rate = FavoriteItem.query.filter_by(user_id=user_id, stock_code=stock_code).first()
    if existing_rate:
        new_rate = rateItem(stock_code=stock_code, user_id=user_id,stock_code=stock_code, rating=rating,content=content)
        db.session.add(new_rate)
        db.session.commit()
        return jsonify({"message": "저장 완료"})
    else:return jsonify({"message": "이미 존재"})
        

@app.route('/stockdetail/ratedelete/<string:stock_code>', methods=['DELETE'])
def stockdetail_ratedelete():
    user_id = session.get('user_id')
    existing_rate = FavoriteItem.query.filter_by(user_id=user_id, stock_code=stock_code).first()
    if existing_rate:
        db.session.delete(existing_rate)
        db.session.commit()
        return jsonify({"message": "Rate deleted"})
    else:
        return jsonify({"message": "없음"}), 404

@app.route('/makelogin', methods=['POST'])
def makelogin():
    salt = 'HZaNK0en1n'
    user_id = request.form['id']
    pw = request.form['pw']
    if not user_id or not pw:
        return render_template('makelogin.html', success=False)
    pw = hashlib.sha512((pw + salt).encode()).hexdigest()
    user = User.query.filter_by(user_id=user_id, user_password=pw).first()
    if user:
        session['user_id'] = user_id
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