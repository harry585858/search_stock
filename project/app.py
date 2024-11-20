from flask import Flask, render_template, request, redirect,request,url_for, session, jsonify
import numpy as np
import json
from config import Config
from flask_cors import CORS
import requests
import hashlib
import sqlite3
#db

app=Flask(__name__)
CORS(app)
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
    if 'logged_in' in session and session['logged_in']:
        return render_template('index.html', logined = True)

    else:
        return render_template('index.html', logined = False)

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
        return render_template('makeresult.html', result=False, error=1)#빈공간 있음
    else:
        pw = pw + salt
        pw = pw.encode()
        pw_hash=hashlib.sha512()
        pw_hash.update(pw)
        pw = pw_hash.hexdigest()
        with sqlite3.connect("database.db") as connection:
            cur = connection.cursor()
            cur.execute("SELECT * FROM user_data WHERE id = ?",(id,))
            user = cur.fetchone()
            if user:
                return render_template('makeresult.html', result=False, error=0)#id 중복
            else:
                cur.execute("INSERT INTO user_data VALUES (?,?,?)",(id,pw,email))
                connection.commit()
                return render_template('makeresult.html',result = True)
@app.route('/makelogin', methods=['POST'])
def makelogin():
    salt = 'HZaNK0en1n'
    id=request.form['id']
    pw=request.form['pw']
    if not id or not pw:
        return render_template('makelogin.html', success=False)#빈공간 있음
    else:
        pw = pw + salt
        pw = pw.encode()
        pw_hash=hashlib.sha512()
        pw_hash.update(pw)
        pw = pw_hash.hexdigest()
        with sqlite3.connect("database.db") as connection:
            cur = connection.cursor()
            cur.execute("SELECT * FROM user_data WHERE id = ? AND pw = ?",(id,pw))
            user = cur.fetchone()
        if user:
            session['user_id']=id
            session['logged_in']=True
            return render_template('makelogin.html', success=True)
        else:
            return render_template('makelogin.html', success=False)#fail
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('logged_in',None)
    return redirect(url_for('login'))
if __name__=='__main__':
    with sqlite3.connect("database.db") as connection:
        cur = connection.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS user_data (id TEXT, pw TEXT, email TEXT)")
        connection.commit()
    app.run(debug=True, port=8000)

    @app.route('/test')
    def test():
        #list ={
        #    {'id':1, 'name':'prj01','currentPrice':10000},{'id':2, 'name':'prj02','currentPrice':20000}
        #}
        #return jsonify(list)

        list = {'message':'test'}
        return jsonify(list)