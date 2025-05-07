import schedule
import pandas as pd
import pymysql
import time
import keras
from datetime import date
from sklearn.preprocessing import MinMaxScaler
from holidayskr import is_holiday

print(__name__)
#현재 파일에서 실행되면 __main__
#다른 파일에서 임포트하면 lstm_result_module

#매일 오후 4시반에 lstm 모델을 이용해 다음날 코스피 지수를 예측하는 함수
def job():
    #주말이랑, 공휴일 제외
    #오늘
    today = date.today()
    #평일
    if is_weekend(today):
        #공휴일
        if is_holiday(str(today)):
            print("평일 공휴일 안돌아감")
            return
    else:
        return
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
    loss = f"{float(loss[0]):.4f}"
    print(f"손실률 : {loss}")
    #mse

    pred = model.predict(kospi)
    result = ans_scaler.inverse_transform(pred.reshape(-1, 1))
    result = result[-1][0]
    result = f"{result:.2f}"
    print(result)

    conn = pymysql.connect(
        host="158.247.211.92",
        user="milk",
        password="0621",
        database="kospi"
    )
    cursor = conn.cursor()
    sql = "insert into finance_notification(title, content) values(%s, %s)"
    cursor.execute(sql, ("주가 예측", f"코스피 지수는 약 {result} 입니다."))
    
    conn.commit()
    
    sql = "insert into predict(date, predict, loss)values(%s, %s, %s)"
    cursor.execute(sql, ("2025-05-02", result, loss))
    
    conn.commit()

    #주가지수 DB에서 꺼내와서 csv에 추가 

#주말 함수
def is_weekend(date):
    return date.weekday() < 5

schedule.every().day.at("16:00").do(job)
    
while True:
    schedule.run_pending()
    time.sleep(1)