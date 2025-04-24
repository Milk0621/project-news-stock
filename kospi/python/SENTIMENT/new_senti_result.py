import pandas as pd

day_news = pd.read_csv("./datas/final/day_news_result.csv")

# day_group_avg = day_news.groupby("date").mean().reset_index()

# result = []
# for idx, ser in day_group_avg.iterrows():
#     max = ser[["0","1","2"]].idxmax()
#     if max == "0":
#         max = "부정"
#     elif max == "1":
#         max = "중립"
#     else:
#         max = "긍정"
#     result.append(max)

# day_group_avg["kor_result"] = result

# day_group_avg.to_csv("./datas/final/senti_result.csv")


#뉴스상세페이지에 LSTM 분석 확률 붙이기

result = []
for idx, ser in day_news.iterrows():
    max = ser[["0","1","2"]].idxmax()
    if max == "0":
        max = "부정"
    elif max == "1":
        max = "중립"
    else:
        max = "긍정"
    result.append(max)


news_data = pd.read_csv("./news_data.csv")
news_data["kor_result"] = result
news_data.to_csv("./datas/pre/pre_news.csv")