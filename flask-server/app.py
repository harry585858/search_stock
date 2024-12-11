from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mail import Mail,Message
import hashlib
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, func, DECIMAL
import os
import requests
from config import Config
from datetime import timedelta
import random
from flask_cors import CORS
import yfinance as yf
from models import *

tickers_list = ['AAPL', 'INTC', 'AMZN', 'META', 'MSFT', 'NVDA', 'TSLA','LOGI','DIS']
stock_name = ['Apple', 'Intel', 'Amazon', 'Meta', 'Microsoft', 'NVIDIA', 'Tesla','Logitech','Disney']
data = yf.download(tickers_list, period="1mo", interval="1d")
modified_Data = []
for time, frame in data.iterrows():
    for ticker in tickers_list:
        modified_Data.append({
            "Datetime": time.strftime('%Y-%m-%d %H:%M'),
            "Ticker": ticker,
            "Name": stock_name[tickers_list.index(ticker)],
            "Open": frame[('Open', ticker)],
            "High": frame[('High', ticker)],
            "Low": frame[('Low', ticker)],
            "Close": frame[('Close', ticker)],
            "AdjClose": frame[('Adj Close', ticker)],
            "Volume": frame[('Volume', ticker)],
        })

#https://github.com/harry585858/search_stock.git

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])
CORS(app, origins=["http://127.0.0.1:3000"])
#내부 데이터베이스 URI 설정 (현재 디렉토리에 example.db 파일 생성)
# basedir = os.path.abspath(os.path.dirname(__file__))  # 현재 파일의 디렉토리 경로
# app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "example.db")}'
# app.config['SECRET_KEY'] = 'password'

# 외부 데이터베이스 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://back:back1234@database-1.c5cys28ymsiz.ap-northeast-2.rds.amazonaws.com:3306/stockDB'

#config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Gmail SMTP 서버
app.config['MAIL_PORT'] = 587  # 포트 번호 (TLS 사용)
app.config['MAIL_USE_TLS'] = True  # TLS 암호화 사용
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'swengineeringtest@gmail.com'  # 이메일 주소
app.config['MAIL_PASSWORD'] = 'wmuoaapdwedxuiyu'  # 이메일 비밀번호
app.config['MAIL_DEFAULT_SENDER'] = 'swengineeringtest@gmail.com'  # 기본 발신자 이메일
mail = Mail(app)  # Mail 객체 초기화
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.secret_key='비밀키'
app.permanent_session_lifetime = timedelta(minutes=30)
homeport = '3000'
homeurl = 'http'+'://127.0.0.1:'+homeport

with app.app_context():
    db.create_all()

# 인증 메일 발송 라우트
@app.route('/verify')
def verify():
    return render_template('send_verification.html')

@app.route('/send_verification', methods=['POST'])
def send_verification():
    email = request.form.get('email')  # 클라이언트가 보낸 이메일 주소
    if not email:
        return jsonify({"error": "이메일이 제공되지 않았습니다."}), 400

    # 랜덤 인증 코드 생성
    verification_code = f"{random.randint(100000, 999999)}"  # 6자리 숫자 코드
    session['verification_code'] = verification_code  # 세션에 저장
    session['email'] = email  # 이메일도 세션에 저장 (추후 검증용)

    # 이메일 전송
    try:
        msg = Message('인증 코드', recipients=[email])
        msg.body = f"인증 코드: {verification_code}\n이 코드를 입력하여 인증을 완료하세요."
        mail.send(msg)
        return render_template('verify_code.html')
    except Exception as e:
        return jsonify({"error": f"이메일 전송 error: {e}"}), 500

# 인증 코드 검증 라우트
@app.route('/verify_code', methods=['POST'])
def verify_code():
    user_code = request.form.get('code')  # 사용자가 입력한 코드
    email = request.form.get('email')  # 이메일
    stored_code = session.get('verification_code')  # 세션에서 저장된 코드 가져오기
    stored_email = session.get('email')  # 세션에 저장된 이메일 가져오기

    if not user_code or not email:
        return jsonify({"error": "코드와 이메일을 제공해주세요."}), 400

    # 코드와 이메일 검증
    if user_code == stored_code and email == stored_email:
        salt = 'HZaNK0en1n'
        user = User.query.filter_by(user_email=email).first()
        user.user_password = hashlib.sha512((request.form.get('pw') + salt).encode()).hexdigest()
        session.pop('verification_code', None)  # 인증 후 코드 삭제
        session.pop('email', None)  # 이메일도 삭제
        return jsonify({"message": "성공!"}), 200
    else:
        return jsonify({"error": "인증 코드가 잘못되었거나 만료되었습니다."}), 400

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

@app.route('/stockdetail/<string:interval>', methods=['POST'])
def stockdetail(interval):
    request_data = request.get_json()
    stock_code = request_data.get("stock_code", None)

    if not stock_code:
        return jsonify ({"error": "Invalid ticker"}), 400

    user_id = session.get('user_id')
    existing_favorite = FavoriteItem.query.filter_by(user_id=user_id, stock_code=stock_code).first()
    avg_rate = db.session.query(func.avg(rateItem.rating)).filter(rateItem.stock_code==stock_code).scalar()
    
    if interval == "week":
        predict_data = [data.to_dict() for data in Oneweekpredict.query.filter_by(stock_code = stock_code).all()]
    elif interval == "month":
        predict_data = [data.to_dict() for data in Onemonthpredict.query.filter_by(stock_code = stock_code).all()]
    else:
        predict_data = [data.to_dict() for data in Onedaypredict.query.filter_by(stock_code = stock_code).all()]
    
    if existing_favorite:
        favorite_status = True
    else:
        favorite_status = False

    if avg_rate:
        return jsonify({"평균평점": avg_rate, "즐겨찾기 여부": favorite_status, "예측데이터": predict_data})
    else:
        return jsonify({"error": "오류"}), 400

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
    rating = request.form.get("rating")
    content = request.form.get("content")
    existing_rate = FavoriteItem.query.filter_by(user_id=user_id, stock_code=stock_code).first()
    if not existing_rate:
        new_rate = rateItem(stock_code=stock_code, user_id=user_id, rating=rating,content=content)
        db.session.add(new_rate)
        db.session.commit()
        return jsonify({"message": "저장 완료"})
    else:
        return jsonify({"message": "이미 존재"})
        

@app.route('/stockdetail/ratedelete/<string:stock_code>', methods=['DELETE'])
def stockdetail_ratedelete(stock_code):
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
        #return render_template('makelogin.html', success=True)
        return redirect(homeurl)
    else:
        return render_template('makelogin.html', success=False)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('logged_in', None)
    return redirect(homeurl)

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
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        favorites = user.favorites
        post = rateItem.query.filter_by(user_id = user_id).all()
        session.permanent = True
        
        return render_template('index.html', logined = True, favorites=favorites, post=post)

    else:
        return render_template('index.html', logined = False)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/makeid')
def makeid():
    return render_template('makeid.html')   

@app.route('/api', methods=['GET'])
def api():
    # 요청에서 ticker 파라미터 추출
    ticker = request.args.get('ticker')
    
    if ticker:  # 특정 티커에 대한 데이터 필터링
        filtered_data = [
            item for item in modified_Data if item['Ticker'] == ticker
        ]
        return jsonify(filtered_data)
    
    # 티커가 없으면 전체 데이터 반환
    return jsonify(modified_Data)

@app.route('/api/predict',methods=['GET'])
def predict():
    ticker=request.args.get('ticker')

    return jsonify(Predictstocks)

if __name__ == '__main__':
    app.run(debug=True, port=8000)