import yfinance as yf
import pandas as pd
from zoneinfo import ZoneInfo
import keras
from sklearn.preprocessing import MinMaxScaler
from datetime import date, timedelta

# #과거 주가지수
# ticker = "^KS11"
# # start = "2025-04-01"
# # end = "2025-04-14"
# cospi = yf.download(ticker, period="730d", interval="60M")
# cospi["date"] = cospi.index

# past = pd.read_csv("./datas/training/kospi.csv")

# cospi.columns = cospi.columns.get_level_values(0)

# cospi = pd.concat([past, cospi], axis=0)

# cospi.to_csv("./datas/training/kospi(60m).csv", index=False)

def LSTM():
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
    print(pred)
    result = ans_scaler.inverse_transform(pred.reshape(-1, 1))
    print(result)

    #1분봉 -> 일봉????????????????????

    #예측값 저장 (날짜 / 예측 / 손실)
    today = date.today()
    # tomorrow = today + timedelta(days=1)
    result = result[0][0]
    loss = loss[0]
    df = [{
        "date" : today,
        "model" : "LSTM",
        "result" : result,
        "loss" : loss
    }]
    prediction = pd.DataFrame(df)
    #저장
    
LSTM()
#스케줄러

