# models.py db관련 클래스 모음
from app import db


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

    def to_dict(self):
        return {
            "id": self.id,
            "stock_code": self.stock_code,
            "price030min": float(self.price30min) if self.price30min else None,
            "price060min": float(self.price60min) if self.price60min else None,
            "price090min": float(self.price90min) if self.price90min else None,
            "price120min": float(self.price120min) if self.price120min else None,
            "price150min": float(self.price150min) if self.price150min else None,
            "price180min": float(self.price180min) if self.price180min else None,
            "price210min": float(self.price210min) if self.price210min else None,
            "price240min": float(self.price240min) if self.price240min else None,
            "price270min": float(self.price270min) if self.price270min else None,
            "price300min": float(self.price300min) if self.price300min else None,
            "price330min": float(self.price330min) if self.price330min else None,
            "price360min": float(self.price360min) if self.price360min else None,
            "price390min": float(self.price390min) if self.price390min else None,
            "price420min": float(self.price420min) if self.price420min else None,
        }

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

    def to_dict(self):
        return {
            "id": self.id,
            "stock_code": self.stock_code,
            "price1day": float(self.price1day) if self.price1day else None,
            "price2day": float(self.price2day) if self.price2day else None,
            "price3day": float(self.price3day) if self.price3day else None,
            "price4day": float(self.price4day) if self.price4day else None,
            "price5day": float(self.price5day) if self.price5day else None,
            "price6day": float(self.price6day) if self.price6day else None,
            "price7day": float(self.price7day) if self.price7day else None,
        }

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

    def to_dict(self):
        return {
            "id": self.id,
            "stock_code": self.stock_code,
            "price03day": float(self.price3day) if self.price3day else None,
            "price06day": float(self.price6day) if self.price6day else None,
            "price09day": float(self.price9day) if self.price9day else None,
            "price12day": float(self.price12day) if self.price12day else None,
            "price15day": float(self.price15day) if self.price15day else None,
            "price18day": float(self.price18day) if self.price18day else None,
            "price21day": float(self.price21day) if self.price21day else None,
            "price24day": float(self.price24day) if self.price24day else None,
            "price27day": float(self.price27day) if self.price27day else None,
            "price30day": float(self.price30day) if self.price30day else None,
        }
  