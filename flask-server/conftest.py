import pytest
from app import create_app  # create_app 함수가 Flask 애플리케이션을 반환하도록 가정

@pytest.fixture
def app():
    app = create_app()  # Flask 애플리케이션 생성
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://back:back1234@database-1.c5cys28ymsiz.ap-northeast-2.rds.amazonaws.com:3306/stockDB'  # 테스트용 메모리 DB 사용
    yield app  # 애플리케이션 인스턴스를 반환
    # 테스트 후 필요한 리소스 정리 (예: DB 세션 종료)
    
@pytest.fixture
def client(app):
    return app.test_client()  # 테스트 클라이언트 반환