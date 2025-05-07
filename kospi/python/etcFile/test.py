# -*- coimport sys
# import sys
# import os
# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# from ML.kobert_finance import kobert_keyword

# text = """
# 코스피가 장중 보합권에서 등락한 끝에 전 거래일 대비 5.00포인트(0.20%) 오른 2,488.42로 장을 마친 21일 오후 서울 중구 하나은행 딜링룸 현황판에 코스피 지수가 표시되고 있다.이날 코스닥 지수는 전 거래일보다 2.32포인트(0.32%) 내린 715.45로 마감했다.
# """

# senti_result, keyword, percent= kobert_keyword(text)
# print(f"senti_result : {senti_result}")
# print(f"keywords : {keyword}")
# print(f"percents : {percent}")

import yfinance as yf
import pandas as pd
data = yf.download("^KS11", period="1d", interval="60M")

print(data)
df = pd.read_csv("./datas/kospi(60m).csv")

if isinstance(data.columns, pd.MultiIndex):  # 멀티인덱스일 경우
    data.columns = data.columns.get_level_values(0)  # 예: ^KS11만 추출
data = data.reset_index()  # Datetime을 일반 열로 변환
data = data.rename(columns={"Datetime": "Date"})  # 열 이름 통일

# 4. 열 순서 정리
data = data[["Close", "High", "Low", "Open", "Volume", "Date"]]

# 5. 기존 CSV와 합치기
combined_df = pd.concat([df, data], ignore_index=True)
print(combined_df)

combined_df.to_csv("./datas/kospi(60m).csv", index=False)