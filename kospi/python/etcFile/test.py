# -*- coimport sys
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from ML.kobert_finance import kobert_keyword
import pandas as pd
import pymysql

conn = pymysql.connect(
    host="158.247.211.92",
    user="milk",
    password="0621",
    database="kospi"
    )
cursor = conn.cursor()

news_df = pd.read_csv("./datas/news_202505072206.csv")
news_df["title"] = news_df["title"].fillna("").astype(str)
news_df["content"] = news_df["content"].fillna("").astype(str)
content = news_df["title"] + news_df["content"]

for idx, text in enumerate(content):
    senti_result, keywords, percentages = kobert_keyword(text)
    print(f"senti_result : {senti_result}")
    print(f"keywords : {keywords}")
    print(f"percents : {percentages}")

    last_row_id = [idx+1] * len(keywords)
    print(last_row_id)
    print(keywords) 
    data = list(zip(last_row_id, keywords))
    
    #뉴스가 인서트됨
    #키워드 테이블에 인서트
    keyword_insert = "insert into keyword(no, keyword) values(%s, %s)"
    cursor.executemany(keyword_insert,(data))
    conn.commit()

    bad, mid, good = percentages
    senti_insert = "insert into senti_result(no, bad, mid, good, result) values(%s, %s, %s, %s, %s)"
    cursor.execute(senti_insert, (last_row_id[0], bad, mid, good, senti_result))
    conn.commit()


# import yfinance as yf
# import pandas as pd
# data = yf.download("^KS11", period="1d", interval="60M")

# print(data)
# df = pd.read_csv("./datas/kospi(60m).csv")

# if isinstance(data.columns, pd.MultiIndex):  # 멀티인덱스일 경우
#     data.columns = data.columns.get_level_values(0)  # 예: ^KS11만 추출
# data = data.reset_index()  # Datetime을 일반 열로 변환
# data = data.rename(columns={"Datetime": "Date"})  # 열 이름 통일

# # 4. 열 순서 정리
# data = data[["Close", "High", "Low", "Open", "Volume", "Date"]]

# # 5. 기존 CSV와 합치기
# combined_df = pd.concat([df, data], ignore_index=True)
# print(combined_df)

# combined_df.to_csv("./datas/kospi(60m).csv", index=False)