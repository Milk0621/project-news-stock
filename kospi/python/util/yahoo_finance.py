import yfinance as yf
import pandas as pd
from zoneinfo import ZoneInfo
import keras
from sklearn.preprocessing import MinMaxScaler

#과거 주가지수
# ticker = "^KS11"
# # start = "2025-04-01"
# # end = "2025-04-14"
# cospi = yf.download(ticker, period="1d", interval="1M")
# cospi["date"] = cospi.index

# past = pd.read_csv("./datas/training/kospi.csv")

# cospi.columns = cospi.columns.get_level_values(0)

# cospi = pd.concat([past, cospi], axis=0)

# cospi.to_csv("./datas/training/kospi.csv", index=False)

model = keras.models.load_model("./model/LSTM_KOSPI.keras")

kospi_df = pd.read_csv("./datas/training/kospi.csv")
kospi = kospi_df[["Close", "Volume", "High", "Low", "Open"]]
scaler = MinMaxScaler(feature_range=(0,1))
data_scaled = scaler.fit_transform(kospi)

ans_scaler = MinMaxScaler(feature_range=(0,1))
close_scaled = ans_scaler.fit_transform(kospi["Close"].to_numpy().reshape(-1, 1))

kospi = data_scaled.reshape(1, data_scaled.shape[0], data_scaled.shape[1])

pred = model.predict(kospi)
print(pred)
pred = ans_scaler.inverse_transform(pred)
print(pred)

#1분봉 -> 일봉????????????????????

#스케줄러