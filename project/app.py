from flask import Flask, render_template, request, redirect,request,url_for, session, jsonify
import numpy as np
import json
from config import Config
import requests
import hashlib

app=Flask(__name__)
app.config['SECRET_KEY']='password'
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/search',methods=['POST'])
def search():
    nameOfStock = {'','','',''}
    nameOfStock = request.form.getlist('nameOfStock[]')
    return render_template('search.html',nameOfStock=nameOfStock)

@app.route('/makeid')
def makeid():
    return render_template('makeid.html')

@app.route('/makeresult',methods=['POST'])
def makeresult():
    salt = 'HZaNK0en1n' 
    id=request.form['id']
    pw=request.form['pw']
    email=request.form['email']
    if not id or not pw or not email:
        return render_template('makeresult.html', result=False)
    else:
        pw = pw + salt
        pw = pw.encode()
        pw_hash=hashlib.sha512()
        pw_hash.update(pw)
        pw = pw_hash.hexdigest()
        return render_template('makeresult.html',result = True)
@app.route('/makelogin', methods=['POST'])
def makelogin():
    id=request.form['id']
    pw=request.form['pw']
    if True:
        return render_template('makelogin.html', success=True)
if __name__=='__main__':
    app.run(debug=True)