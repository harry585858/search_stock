import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_hello_world(client):
    # GET 요청을 보냄
    response = client.get('/')
    # 응답 코드가 200(성공)인지 확인
    assert response.status_code == 200

def makelogin(client):
    #  요청을 보냄
    data= {'id':"abc", 'pw':'1234'}
    response = client.post('/makelogin')
    # 응답 코드가 200(성공)인지 확인
    assert response.status_code == 200

def logout(client):
    response = client.get('/logout')
    # 응답 코드가 200(성공)인지 확인
    assert response.status_code == 200

def makeresult(client): #회원가입
    data= {'id':"abc", 'pw':'1234', 'email':'1234@1234'}
    response = client.post('/makeresult')
    # 응답 코드가 200(성공)인지 확인
    assert response.status_code == 200
def verify(client):
    data= {'email':'1234@1234'}
    response = client.post('/email_verification')
    assert response.status_code == 200
def mypage(client):
    response = client.post('/email_verification')
    assert response.status_code == 200
def favorite(client):
    response = client.post('stockdetail/favorite/AAPL')
    assert response.status_code == 200
def favorite1(client):
    response = client.delete('stockdetail/favorite/AAPL')
    assert response.status_code == 200
def favorite1(client):
    response = client.get('/naver/login')
    assert response.status_code == 200
def detail(client):
    response = client.get('/stockdetails/month')
    assert response.status_code == 200
def apii(client):
    response = client.get('/api')
    assert response.status_code == 200
def apip(client):
    response = client.get('/api/predict?ticker=AAPL')
    assert response.status_code == 200