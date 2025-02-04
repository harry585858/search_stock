# -*- coding: utf-8 -*-
"""LSTM 예측모델.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1eKvfWVs0eKX5Dxm1pcnnMYvESJxh21yG

#필요한 라이브러리 설치
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import os

# %matplotlib inline
warnings.filterwarnings('ignore')

import FinanceDataReader as fdr

# 기업명과 종목 코드 리스트
companies = {
    '애플': 'AAPL',
    '테슬라': 'TSLA',
    '엔비디아': 'NVDA',
    '인텔': 'INTC',
    '아마존': 'AMZN',
    '메타 플랫폼스': 'META',
    '로지텍': 'LOGI',
    '마이크로소프트': 'MSFT',
    '디즈니': 'DIS'
}

# 각 기업의 데이터를 저장할 데이터프레임 딕셔너리
company_data = {}

# 각 기업의 주가 데이터를 가져와 저장
for name, ticker in companies.items():
    try:
        df = fdr.DataReader(ticker)
        company_data[name] = df
        print(f"{name} ({ticker}) 데이터 가져오기 성공")
    except Exception as e:
        print(f"{name} ({ticker}) 데이터 가져오기 실패: {e}")

# 가져온 데이터 예시 출력
for name, df in company_data.items():
    print(f"\n{name} 주가 데이터 (최근 5일):")
    print(df.tail(5))

"""#전처리"""

from sklearn.preprocessing import MinMaxScaler

apple = fdr.DataReader('AAPL')
scaler = MinMaxScaler()
# 스케일을 적용할 column을 정의합니다.
scale_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
# 스케일 후 columns
scaled = scaler.fit_transform(apple[scale_cols])
scaled

df = pd.DataFrame(scaled, columns=scale_cols)

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(df.drop('Close', axis = 1), df['Close'], test_size=0.2, random_state=0, shuffle=False)

x_train.shape, y_train.shape
x_test.shape, y_test.shape
x_train

import tensorflow as tf
def windowed_dataset(series, window_size, batch_size, shuffle):
    series = tf.expand_dims(series, axis=-1)
    ds = tf.data.Dataset.from_tensor_slices(series)
    ds = ds.window(window_size + 1, shift=1, drop_remainder=True)
    ds = ds.flat_map(lambda w: w.batch(window_size + 1))
    if shuffle:
        ds = ds.shuffle(1000)
    ds = ds.map(lambda w: (w[:-1], w[-1]))
    return ds.batch(batch_size).prefetch(1)

WINDOW_SIZE=20
BATCH_SIZE=32

train_data = windowed_dataset(y_train, WINDOW_SIZE, BATCH_SIZE, True)
test_data = windowed_dataset(y_test, WINDOW_SIZE, BATCH_SIZE, False)

for data in train_data.take(1):
    print(f'데이터셋(X) 구성(batch_size, window_size, feature갯수): {data[0].shape}')
    print(f'데이터셋(Y) 구성(batch_size, window_size, feature갯수): {data[1].shape}')

"""#예측모델"""

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Conv1D, Lambda
from tensorflow.keras.losses import Huber
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint


model = Sequential([
    # 1차원 feature map 생성
    Conv1D(filters=32, kernel_size=5,
           padding="causal",
           activation="relu",
           input_shape=[WINDOW_SIZE, 1]),
    # LSTM
    LSTM(16, activation='tanh'),
    Dense(16, activation="relu"),
    Dense(1),
])

# Sequence 학습에 비교적 좋은 퍼포먼스를 내는 Huber()를 사용합니다.
loss = Huber()
optimizer = Adam(0.0005)
model.compile(loss=Huber(), optimizer=optimizer, metrics=['mse'])

# earlystopping은 10번 epoch통안 val_loss 개선이 없다면 학습을 멈춥니다.
earlystopping = EarlyStopping(monitor='val_loss', patience=10)
# val_loss 기준 체크포인터도 생성합니다.
filename = os.path.join('tmp', 'ckeckpointer.weights.h5')
checkpoint = ModelCheckpoint(filename,
                             save_weights_only=True,
                             save_best_only=True,
                             monitor='val_loss',
                             verbose=1)

history = model.fit(train_data,
                    validation_data=(test_data),
                    epochs=50,
                    callbacks=[checkpoint, earlystopping])

model.load_weights(filename)
pred = model.predict(test_data)
pred.shape

#데이터 시각화
plt.figure(figsize=(12, 9))
plt.plot(np.asarray(y_test)[100:], label='actual')
plt.plot(pred, label='prediction')
plt.legend()
plt.show()

# Create a DataFrame for comparison
y_test_data = np.asarray(y_test)[100:]  # Actual values
pred_data = pred  # Predicted values

# Ensure both arrays have the same length for comparison
min_length = min(len(y_test_data), len(pred_data))
y_test_data = y_test_data[:min_length]
pred_data = pred_data[:min_length]

df_results = pd.DataFrame({
    'Actual': y_test_data.flatten(),
    'Prediction': pred_data.flatten()
})

# Print the results table
print(df_results)

"""#데이터 베이스 삽입"""

# 실제 주식 데이터로 스케일러를 학습시킴
stock_data = apple['Close'].values.reshape(-1, 1)  # 실제 주식 데이터 예시
scaler = MinMaxScaler()
scaler.fit(stock_data)

# 실제 주식 데이터에서 최소값과 최대값을 설정
actual_min = stock_data.min()
actual_max = stock_data.max()

# 모델 예측 및 복원 과정
# 예를 들어 30일간의 예측을 수행한다고 가정
days_to_predict = 30
predictions_scaled = []

# y_test의 마지막 부분을 사용하여 초기 입력 데이터 준비
last_sequence = y_test[-WINDOW_SIZE:].values
last_sequence_scaled = scaler.transform(last_sequence.reshape(-1, 1)).reshape(1, WINDOW_SIZE, 1)

for day in range(days_to_predict):
    # 하루 예측
    predicted_value_scaled = model.predict(last_sequence_scaled)[0][0]  # 예측된 값 추출
    predictions_scaled.append(predicted_value_scaled)

    # 다음 날 예측을 위해 시퀀스 업데이트
    last_sequence_scaled = np.roll(last_sequence_scaled, -1)  # 데이터를 왼쪽으로 한 칸 이동
    last_sequence_scaled[0, -1, 0] = predicted_value_scaled  # 가장 최근 예측 값을 입력에 추가


# 예측 값을 원래 스케일로 복원
predictions = scaler.inverse_transform(np.array(predictions_scaled).reshape(-1, 1)).flatten()

# 정규화된 예측 값을 원래 스케일로 역변환
predictions_dollar_values = predictions * (actual_max - actual_min) + actual_min

print("예측된 달러 값:")
print(predictions_dollar_values)

# 예측 결과를 DataFrame으로 정리하고 출력
dates = pd.date_range(start=pd.Timestamp("today") + pd.Timedelta(days=1), periods=days_to_predict, freq='D')
df_predictions = pd.DataFrame({'Date': dates, 'Predicted_Close': predictions_dollar_values})

# 예측 값을 두 자리 소수점으로 반올림
df_predictions['Predicted_Close'] = df_predictions['Predicted_Close'].round(2)
# monthly_prices 리스트에 예측 값 저장
monthly_prices = df_predictions['Predicted_Close'].tolist()

print("한 달 예측 결과 (하루 단위):")
print(df_predictions)

# 시각화
plt.figure(figsize=(12, 6))
plt.plot(df_predictions['Date'], df_predictions['Predicted_Close'], label="Predicted Close Price", color="green")
plt.xlabel("Date")
plt.ylabel("Predicted Close Price")
plt.title("30-Day Forecast of Stock Price (Starting from Today)")
plt.legend()
plt.show()


# Flask 및 SQLAlchemy 설정
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DECIMAL

# Flask 앱 및 SQLAlchemy 설정
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://lstm:lstm1234@database-1.c5cys28ymsiz.ap-northeast-2.rds.amazonaws.com:3306/stockDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Predictstocks 테이블 정의
class Predictstocks(db.Model):
    __tablename__ = 'Predictstocks'
    id = db.Column(db.Integer, primary_key=True)
    stock_name = db.Column(db.String(20), nullable=False)
    stock_code = db.Column(db.String(20), unique=True, nullable=False)  # unique constraint for foreign key

### OnemonthPredictTest 테이블 정의 (Predictstocks와 외래 키 연결)
class Oneweekpredict(db.Model):
    __tablename__ = 'Oneweekpredict'
    id = db.Column(db.Integer, primary_key=True)
    stock_code = db.Column(db.String(20), db.ForeignKey('Predictstocks.stock_code'))
    price1day = db.Column(DECIMAL(10, 2))
    price2day = db.Column(DECIMAL(10, 2))
    price3day = db.Column(DECIMAL(10, 2))
    price4day = db.Column(DECIMAL(10, 2))
    price5day = db.Column(DECIMAL(10, 2))
    price6day = db.Column(DECIMAL(10, 2))
    price7day = db.Column(DECIMAL(10, 2))

# OnemonthPredictTest 테이블 정의 (Predictstocks와 외래 키 연결)
class Onemonthpredict(db.Model):
    __tablename__ = 'Onemonthpredict'
    id = db.Column(db.Integer, primary_key=True)
    stock_code = db.Column(db.String(20), db.ForeignKey('Predictstocks.stock_code'))
    price3day = db.Column(DECIMAL(10, 2))
    price6day = db.Column(DECIMAL(10, 2))
    price9day = db.Column(DECIMAL(10, 2))
    price12day = db.Column(DECIMAL(10, 2))
    price15day = db.Column(DECIMAL(10, 2))
    price18day = db.Column(DECIMAL(10, 2))
    price21day = db.Column(DECIMAL(10, 2))
    price24day = db.Column(DECIMAL(10, 2))
    price27day = db.Column(DECIMAL(10, 2))
    price30day = db.Column(DECIMAL(10, 2))

"""# 데이터베이스 생성
with app.app_context():
    db.create_all()
    print("테이블 생성 완료")"""

# 데이터 삽입 함수 정의
def insert_test_data():
    stock_code = 'AAPL'
    stock_name = 'Apple Inc.'

    # 먼저 Predictstocks 테이블에 stock_code를 삽입하여 외래 키 참조를 만족시킴
    with app.app_context():
        # Predictstocks에 stock_code가 없으면 삽입
        if not Predictstocks.query.filter_by(stock_code=stock_code).first():
            new_stock = Predictstocks(stock_name=stock_name, stock_code=stock_code)
            db.session.add(new_stock)
            db.session.commit()
            print(f"New stock entry added for {stock_code}")


        existing_entry = Onemonthpredict.query.filter_by(stock_code=stock_code).first()
        if existing_entry:
            # 업데이트하는 경우
            existing_entry.price3day = monthly_prices[2]
            existing_entry.price6day = monthly_prices[5]
            existing_entry.price9day = monthly_prices[8]
            existing_entry.price12day = monthly_prices[11]
            existing_entry.price15day = monthly_prices[14]
            existing_entry.price18day = monthly_prices[17]
            existing_entry.price21day = monthly_prices[20]
            existing_entry.price24day = monthly_prices[23]
            existing_entry.price27day = monthly_prices[26]
            existing_entry.price30day = monthly_prices[29]
            print("Data updated for stock_code:", stock_code)
        else:
            # 새로운 데이터 삽입
            new_entry = Onemonthpredict(
                stock_code=stock_code,
                price3day=monthly_prices[2],
                price6day=monthly_prices[5],
                price9day=monthly_prices[8],
                price12day=monthly_prices[11],
                price15day=monthly_prices[14],
                price18day=monthly_prices[17],
                price21day=monthly_prices[20],
                price24day=monthly_prices[23],
                price27day=monthly_prices[26],
                price30day=monthly_prices[29]
            )
            db.session.add(new_entry)
            print("New data inserted for stock_code:", stock_code)

        # Oneweekpredict 테이블에 데이터 삽입/업데이트
        existing_entry_week = Oneweekpredict.query.filter_by(stock_code=stock_code).first()
        if existing_entry_week:
            # 업데이트하는 경우
            existing_entry_week.price1day = monthly_prices[0]
            existing_entry_week.price2day = monthly_prices[1]
            existing_entry_week.price3day = monthly_prices[2]
            existing_entry_week.price4day = monthly_prices[3]
            existing_entry_week.price5day = monthly_prices[4]
            existing_entry_week.price6day = monthly_prices[5]
            existing_entry_week.price7day = monthly_prices[6]
            print("Data updated for stock_code:", stock_code, "in Oneweekpredict")
        else:
            # 새로운 데이터 삽입
            new_entry_week = Oneweekpredict(
                stock_code=stock_code,
                price1day=monthly_prices[0],
                price2day=monthly_prices[1],
                price3day=monthly_prices[2],
                price4day=monthly_prices[3],
                price5day=monthly_prices[4],
                price6day=monthly_prices[5],
                price7day=monthly_prices[6]
            )
            db.session.add(new_entry_week)
            print("New data inserted for stock_code:", stock_code, "in Oneweekpredict")

        db.session.commit()
        db.session.commit()

# 데이터 삽입 실행
insert_test_data()

# 모델 생성
WINDOW_SIZE = 20
model = Sequential([
    LSTM(50, activation='tanh', return_sequences=False, input_shape=(WINDOW_SIZE, 1)),
    Dense(1)
])
model.compile(optimizer='adam', loss='mse')

# 조정 로직
def adjust_predictions(predictions, scaler, max_deviation=0.05):
    """
    예측값을 조정하여 지나치게 큰 값이 나오지 않도록 제한.
    :param predictions: 모델의 예측값 (스케일링된 상태)
    :param scaler: MinMaxScaler 객체
    :param max_deviation: 허용할 최대 편차 비율 (기본값: 5%)
    :return: 조정된 예측값 리스트
    """
    predictions_original = scaler.inverse_transform(np.array(predictions).reshape(-1, 1)).flatten()
    adjusted_predictions = []
    for i, value in enumerate(predictions_original):
        if i == 0:
            adjusted_predictions.append(value)
        else:
            max_value = adjusted_predictions[-1] * (1 + max_deviation)
            min_value = adjusted_predictions[-1] * (1 - max_deviation)
            adjusted_predictions.append(max(min(value, max_value), min_value))
    return scaler.transform(np.array(adjusted_predictions).reshape(-1, 1)).flatten()

# 전체 주식 예측 함수
def insert_all_stocks_predictions(companies):
    for name, ticker in companies.items():
        try:
            print(f"\nProcessing {name} ({ticker})...")
            # Step 1: 데이터 가져오기
            stock_data = pd.DataFrame({
                "Close": np.random.uniform(100, 200, 300)  # 가상 데이터 (실제 구현 시 FinanceDataReader 사용)
            })

            # 'Close' 피처만 사용
            close_data = stock_data[['Close']].values
            scaler = MinMaxScaler()
            scaled_close_data = scaler.fit_transform(close_data)

            # Step 2: 데이터셋 분리
            train_size = int(len(scaled_close_data) * 0.8)
            train_data = scaled_close_data[:train_size]
            test_data = scaled_close_data[train_size:]

            # Step 3: Windowed 데이터 생성
            def create_windowed_data(data, window_size):
                X, y = [], []
                for i in range(len(data) - window_size):
                    X.append(data[i:i + window_size])
                    y.append(data[i + window_size])
                return np.array(X), np.array(y)

            X_train, y_train = create_windowed_data(train_data, WINDOW_SIZE)
            X_test, y_test = create_windowed_data(test_data, WINDOW_SIZE)

            # Step 4: 모델 훈련
            print(f"Training model for {name} ({ticker})...")
            model.fit(X_train, y_train, epochs=10, verbose=1, validation_data=(X_test, y_test))

            # Step 5: 30일 예측
            last_sequence = test_data[-WINDOW_SIZE:]
            predictions_scaled = []
            for day in range(30):
                predicted_value_scaled = model.predict(last_sequence.reshape(1, WINDOW_SIZE, 1))[0][0]
                predictions_scaled.append(predicted_value_scaled)
                last_sequence = np.roll(last_sequence, -1)
                last_sequence[-1] = predicted_value_scaled

            # 예측값 조정
            adjusted_predictions_scaled = adjust_predictions(predictions_scaled, scaler)
            predictions = scaler.inverse_transform(np.array(adjusted_predictions_scaled).reshape(-1, 1)).flatten()

            # Step 6: 데이터베이스 삽입
            with app.app_context():
                if not Predictstocks.query.filter_by(stock_code=ticker).first():
                    new_stock = Predictstocks(stock_name=name, stock_code=ticker)
                    db.session.add(new_stock)
                    db.session.commit()

                existing_entry = Onemonthpredict.query.filter_by(stock_code=ticker).first()
                if existing_entry:
                    existing_entry.price3day = predictions[2]
                    existing_entry.price6day = predictions[5]
                    existing_entry.price9day = predictions[8]
                    existing_entry.price12day = predictions[11]
                    existing_entry.price15day = predictions[14]
                    existing_entry.price18day = predictions[17]
                    existing_entry.price21day = predictions[20]
                    existing_entry.price24day = predictions[23]
                    existing_entry.price27day = predictions[26]
                    existing_entry.price30day = predictions[29]
                else:
                    new_entry = Onemonthpredict(
                        stock_code=ticker,
                        price3day=predictions[2],
                        price6day=predictions[5],
                        price9day=predictions[8],
                        price12day=predictions[11],
                        price15day=predictions[14],
                        price18day=predictions[17],
                        price21day=predictions[20],
                        price24day=predictions[23],
                        price27day=predictions[26],
                        price30day=predictions[29]
                    )
                    db.session.add(new_entry)

                db.session.commit()
                print(f"Data for {name} ({ticker}) successfully updated in database!")

        except Exception as e:
            print(f"Error processing {name} ({ticker}): {e}")

# 실행
# 기업명과 종목 코드 리스트
companies = {
    '애플': 'AAPL',
    '테슬라': 'TSLA',
    '엔비디아': 'NVDA',
    '인텔': 'INTC',
    '아마존': 'AMZN',
    '메타 플랫폼스': 'META',
    '로지텍': 'LOGI',
    '마이크로소프트': 'MSFT',
    '디즈니': 'DIS'
}
insert_all_stocks_predictions(companies)
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DECIMAL

# Flask 설정 및 데이터베이스 초기화
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://lstm:lstm1234@database-1.c5cys28ymsiz.ap-northeast-2.rds.amazonaws.com:3306/stockDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Onedaypredict 테이블 정의
class Onedaypredict(db.Model):
    __tablename__ = 'Onedaypredict'
    id = db.Column(db.Integer, primary_key=True)
    stock_code = db.Column(db.String(20), unique=True, nullable=False)
    price30min = db.Column(DECIMAL(10, 2))
    price60min = db.Column(DECIMAL(10, 2))
    price90min = db.Column(DECIMAL(10, 2))
    price120min = db.Column(DECIMAL(10, 2))
    price150min = db.Column(DECIMAL(10, 2))
    price180min = db.Column(DECIMAL(10, 2))
    price210min = db.Column(DECIMAL(10, 2))
    price240min = db.Column(DECIMAL(10, 2))
    price270min = db.Column(DECIMAL(10, 2))
    price300min = db.Column(DECIMAL(10, 2))
    price330min = db.Column(DECIMAL(10, 2))
    price360min = db.Column(DECIMAL(10, 2))
    price390min = db.Column(DECIMAL(10, 2))
    price420min = db.Column(DECIMAL(10, 2))

# 데이터 전처리 함수
def preprocess_data(data, window_size=20):
    if len(data) < window_size:
        raise ValueError(f"Not enough data to preprocess. Available: {len(data)}, Required: {window_size}")
    
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data.values.reshape(-1, 1))

    X, y = [], []
    for i in range(len(scaled_data) - window_size):
        X.append(scaled_data[i:i + window_size])
        y.append(scaled_data[i + window_size])
    return np.array(X), np.array(y), scaler

# LSTM 모델 생성 및 학습
def build_and_train_model(X_train, y_train, X_test, y_test):
    model = Sequential([
        LSTM(50, activation='tanh', return_sequences=False, input_shape=(X_train.shape[1], 1)),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test), verbose=1)
    return model

# 예측 함수
def predict_future(model, last_sequence, scaler, steps=14):
    predictions = []
    sequence = last_sequence.copy()
    for _ in range(steps):
        predicted_value = model.predict(sequence.reshape(1, -1, 1))[0][0]
        predictions.append(predicted_value)
        sequence = np.roll(sequence, -1)
        sequence[-1] = predicted_value
    predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1)).flatten()
    return predictions

# 데이터베이스 삽입 함수
def insert_predictions_to_db(stock_code, predictions):
    with app.app_context():
        entry = Onedaypredict.query.filter_by(stock_code=stock_code).first()
        if entry:
            for i, field in enumerate(entry.__table__.columns.keys()[2:]):
                setattr(entry, field, predictions[i])
        else:
            new_entry = Onedaypredict(stock_code=stock_code, **{f"price{(i+1)*30}min": predictions[i] for i in range(len(predictions))})
            db.session.add(new_entry)
        db.session.commit()

# 메인 실행 함수
def main():
    companies = {
        '애플': 'AAPL',
        '테슬라': 'TSLA',
        '엔비디아': 'NVDA',
        '인텔': 'INTC',
        '아마존': 'AMZN',
        '메타 플랫폼스': 'META',
        '로지텍': 'LOGI',
        '마이크로소프트': 'MSFT',
        '디즈니': 'DIS'
    }

    for name, ticker in companies.items():
        print(f"\nProcessing {name} ({ticker})...")
        try:
            # 데이터 가져오기
            data = yf.download(ticker, interval='1m', period='5d')
            if data.empty or 'Close' not in data.columns:
                raise ValueError(f"No valid data for {ticker}. Check ticker and interval settings.")

            close_data = data['Close']
            print(f"{name} 데이터 가져오기 완료: {close_data.tail()}")

            # 데이터 전처리
            window_size = 20
            X, y, scaler = preprocess_data(close_data, window_size)

            # 데이터 분리
            train_size = int(len(X) * 0.8)
            X_train, y_train = X[:train_size], y[:train_size]
            X_test, y_test = X[train_size:], y[train_size:]

            if len(X_test) == 0:
                raise ValueError(f"No test data available for {ticker}. Skipping this stock.")

            # 모델 생성 및 학습
            model = build_and_train_model(X_train, y_train, X_test, y_test)

            # 예측 수행
            last_sequence = X_test[-1]
            predictions = predict_future(model, last_sequence, scaler, steps=14)

            # 데이터베이스에 예측값 삽입
            insert_predictions_to_db(ticker, predictions)
            print(f"{name} ({ticker}) 예측값 데이터베이스 저장 완료.")

        except Exception as e:
            print(f"Error processing {name} ({ticker}): {e}")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # 테이블 생성
    main()
