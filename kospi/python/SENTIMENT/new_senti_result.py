import pandas as pd

day_news = pd.read_csv("./datas/final/day_news_result.csv")
print(day_news)
day_group_avg = day_news.groupby("date").mean().reset_index()
print(day_group_avg)
for idx, ser in day_group_avg.iterrows():
    print(ser[["0","1","2"]].idxmax())
    #print(ser)
    #print(i)
# for date in range(len(day_group_avg)):
#     day = day_group_avg["date"][date]
#     bad = day_group_avg["0"][date]
#     mid = day_group_avg["1"][date]
#     good = day_group_avg["2"][date]
#     print(day, bad, mid, good)
#     if bad > mid | bad > good:
#         day_group_avg["result"][date] = "부정"