import pandas as pd
import re

#크롤링한 데이터
keywords = pd.read_csv("./datas/final/keywords.csv")

date = keywords["date"].drop_duplicates()

result= []
for i in date:
    date_word = keywords[keywords["date"] == i]
    
    #날짜별 전체 개수
    total_cnt = date_word["word_type"].count()
    
    #타입 그룹화
    type = date_word.groupby("word_type").agg('count').reset_index()
    print(type)
    bad = type[type["word_type"]==0]
    mid = type[type["word_type"]==1]
    good = type[type["word_type"]==2]
    print(good["keyword"])
    # print(good["keyword"].values)
    #감정분석 결과 (긍정, 부정, 중립)
    good_per = (good["keyword"].values/total_cnt)*100 
    # print(good_per["keyword"].values)
    mid_per = (mid["keyword"].values/total_cnt)*100 
    bad_per = (bad["keyword"].values/total_cnt)*100 
    print(good_per)
    if good_per > bad_per:
        dict = {
            "date" : i,
            "result" : "긍정",
            "good" : good_per,
            "mid" : mid_per,
            "bad" : bad_per
        }
    elif good_per < bad_per:
        dict = {
            "date" : i,
            "result" : "부정",
            "good" : good_per,
            "mid" : mid_per,
            "bad" : bad_per
        }
    else:
        dict = {
            "date" : i,
            "result" : "중립",
            "good" : good_per,
            "mid" : mid_per,
            "bad" : bad_per
        }
    result.append(dict)
df = pd.DataFrame(result)
df.to_csv("./datas/final/senti_result.csv", index=False)