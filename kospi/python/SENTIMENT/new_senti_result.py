import pandas as pd

day_news = pd.read_csv("./datas/final/day_news_result.csv")

day_group_avg = day_news.groupby("date").mean().reset_index()

result = []
for idx, ser in day_group_avg.iterrows():
    max = ser[["0","1","2"]].idxmax()
    if max == "0":
        max = "부정"
    elif max == "1":
        max = "중립"
    else:
        max = "긍정"
    result.append(max)

day_group_avg["kor_result"] = result

day_group_avg.to_csv("./datas/final/senti_result.csv")