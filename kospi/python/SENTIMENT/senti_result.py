import pandas as pd
from konlpy.tag import Okt
import re

#크롤링한 데이터
news = pd.read_csv("./datas/final/keywords.csv")

# dfs = news.groupby(["date"]).sum().reset_index()
# print(dfs)



#SQL
