import schedule
import pandas as pd
import pymysql
import time
import keras
from datetime import date
from sklearn.preprocessing import MinMaxScaler

#매일 오후 4시반에 lstm 모델을 이용해 다음날 코스피 지수를 예측하는 함수
def job():
    #모델 로드해서 결과치 뽑아내기
    model = keras.models.load_model("./model/LSTM_KOSPI.keras")
    kospi_df = pd.read_csv("./datas/training/kospi(60m).csv")
    kospi = kospi_df[["Close", "Volume", "High", "Low", "Open"]]
    scaler = MinMaxScaler(feature_range=(0,1))
    data_scaled = scaler.fit_transform(kospi)
    ans_scaler = MinMaxScaler(feature_range=(0,1))
    close_scaled = ans_scaler.fit_transform(kospi["Close"].to_numpy().reshape(-1, 1))
    close_shape = close_scaled.shape[0]

    kospi = data_scaled.reshape(1, data_scaled.shape[0], data_scaled.shape[1])

    #모델 평가
    loss = model.evaluate(kospi, close_scaled.reshape(1, close_shape, 1), verbose=1)
    #테스트데이터를 이용한 모델 점수 평가
    print(f"손실률 : {loss}")

    pred = model.predict(kospi)
    result = ans_scaler.inverse_transform(pred.reshape(-1, 1))
    result = result[-1][0]

    #예측값 저장 (날짜 / 예측 / 손실)
    # today = date.today()
    # # tomorrow = today + timedelta(days=1)
    # result = result[0][0]
    # loss = loss[0]
    # df = [{
    #     "date" : today,
    #     "model" : "LSTM",
    #     "result" : result,
    #     "loss" : loss
    # }]
    # print('내일 주가 알림', f'내일 코스피 지수는 약 {result} 입니다.')

    conn = pymysql.connect(
        host="158.247.211.92",
        user="milk",
        password="0621",
        database="kospi"
    )
    cursor = conn.cursor()
    sql = "insert into finance_notification(title, content) values(%s, %s)"
    cursor.execute(sql, ("내일 주가 알림", f"내일 코스피 지수는 약 {result} 입니다."))
    conn.commit()

schedule.every().day.at("17:01").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)