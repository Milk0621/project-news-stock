import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from ML.kobert_finance import kobert_keyword
import pymysql

df = pd.read_csv("news_data2.csv")

content = df["content"]
print(content)

conn = pymysql.connect(
    host="158.247.211.92",
    user="milk",
    password="0621",
    database="kospi"
    )
cursor = conn.cursor()

for i, _ in enumerate(content):
    senti_result, keywords, percentages = kobert_keyword(content)
    print(senti_result, keywords) 

    last_row_id = [i+1] * len(keywords)
    print(last_row_id)
    data = list(zip(i+1, keywords))
    print(data)
    #뉴스가 인서트됨
    #키워드 테이블에 인서트
    # keyword_insert = "insert into keyword(no, keyword) values(%s, %s)"
    # cursor.executemany(keyword_insert,(data))
    # conn.commit()

    bad, mid, good = percentages
    print(bad, mid, good)
    # senti_insert = "insert into senti_result(no, bad, mid, good, result) values(%s, %s, %s, %s, %s)"
    # cursor.execute(senti_insert, (i+1, bad, mid, good, senti_result))
    # conn.commit()