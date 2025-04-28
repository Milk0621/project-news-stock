import pandas as pd
import numpy as np
#import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

kospi_df = pd.read_csv("./datas/training/kospi(60m).csv")

close = kospi_df[["Close", "Volume", "High", "Low", "Open"]]

print(close)

scaler = MinMaxScaler(feature_range=(0,1))
data_scaled = scaler.fit_transform(close)
#0 ~ 1사이로 데이터 정규화
#[[50000]] X -> [[50000    20000     40000     50000]]
#(1227, 5)

ans_scaler = MinMaxScaler(feature_range=(0,1))
close_scaled = ans_scaler.fit_transform(close["Close"].to_numpy().reshape(-1, 1))
#[2118, 2157, 2165] -> #[[2118  2157  2165]]

X = data_scaled.reshape(1, data_scaled.shape[0], data_scaled.shape[1])

# X = X[:, :-5, :]
# pred_data = X[:, -5:, :]

y = np.array([data_scaled[-1, 0]])
#[[1227]]
# print(pred_data)

# print(X.shape)
# print(data_scaled.shape)

import keras

model = keras.Sequential()
lstm = keras.layers.LSTM(100, return_sequences=True, input_shape=(data_scaled.shape[0], data_scaled.shape[1]))

dense = keras.layers.Dense(100, activation="relu")

dropout = keras.layers.Dropout(0.2)

output = keras.layers.Dense(1)

model.add(lstm)
model.add(dense)
model.add(dropout)
model.add(output)

model.compile(loss="mse", metrics=["mae"], optimizer="adam")

#print(model.summary())

model.fit(X, y, epochs=40, verbose=1)
#[0.5735805  0.06647381 0.56756122 0.56978139]]]

model.save("./model/LSTM_KOSPI.keras")

# print(X[:,-1 :, :])
# pred = model.predict(pred_data)

# """
# [[
#     [2000  50000  60000   20000  20000]
#     [2000  50000  60000   20000  20000]
#     [2000  50000  60000   20000  20000]
# ]]
# """
# print(pred)
# pred = ans_scaler.inverse_transform(pred)
# print(pred)