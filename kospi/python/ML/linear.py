import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

#데이터 불러오기
kospi_df = pd.read_csv("./datas/training/kospi.csv")

#선형회귀 모델에 문자열 값이 들어갈 수 없으므로
#날짜를 datetime 형식으로 변환
kospi_df["Date"] = pd.to_datetime(kospi_df["Date"])
 
kospi_df["Year"] = kospi_df["Date"].dt.year
kospi_df["Month"] = kospi_df["Date"].dt.month
kospi_df["Day"] = kospi_df["Date"].dt.day
kospi_df["Weekday"] = kospi_df["Date"].dt.weekday
#[1,2,3,4,5,6] -> 시작가, 고가, 저가, 거래량, 연 월 일 -> 다음날 종가


#입력데이터, 정답데이터
X = kospi_df[["Open", "High", "Low", "Volume", "Year", "Month", "Day", "Weekday"]].to_numpy()
y = kospi_df["Close"].shift(-1).to_numpy()
#오늘의 데이터로 다음날의 종가를 예측해야하므로 정답데이터를 하나씩 땡김

today_x = X[-1:]
#어제 데이터

#한칸씩 땡기면 마지막 종가에 빈칸이 생기기 때문에 마지막행 삭제
X = X[:-1]
y = y[:-1]

print(X.shape)
print(y.shape)

train_input, test_input, train_target, test_target = train_test_split(X, y)

lr = LinearRegression()
lr.fit(train_input, train_target)
print("Train score:", lr.score(train_input, train_target))
print("Test score:", lr.score(test_input, test_target))

y_hat = lr.predict(test_input)
y = test_target
#mean_squared_error : 머신러닝 손실률 계산하는 애
loss = mean_squared_error(y, y_hat)
print(loss)

#예측 결과
pred = lr.predict(today_x)
print(pred)