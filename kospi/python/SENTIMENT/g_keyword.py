# -*- coding: utf-8 -*- 
import pandas as pd
from konlpy.tag import Okt
import re

#단어 사전
total_dict = pd.read_csv("./datas/dict/total_dict.csv")

#크롤링한 데이터
news = pd.read_csv("./news_data.csv")

#불용어
stopwords = pd.read_csv("./datas/dict/stopwords-ko.txt")

okt = Okt()

#전처리
def text_process(text):
    creaned = re.sub(r"[^ㄱ-ㅎ가-힣\s]", "", text)
    tokens = okt.morphs(creaned, stem=True)
    filtered = [t for t in tokens if t not in stopwords]
    result = " ".join(filtered)
    return result

contents = news["content"].astype(str)
tokens = [text_process(content) for content in contents]

keyword = []

senti_score = []

for idx, token in enumerate(tokens):
    print(f"{idx}번 뉴스 데이터 처리")
    sentiment = 0
    for i in range(0, len(total_dict)):
        if total_dict.word[i] in token:
            sentiment += int(total_dict.score[i])
            if int(total_dict.score[i]) > 0:
                keyword.append(
                    {
                        "date" : news.loc[idx, "date"],
                        "keyword" : total_dict.word[i],
                        "word_type" : 2
                    }
                             )
            elif int(total_dict.score[i]) < 0:
                keyword.append(
                    {
                        "date" : news.loc[idx, "date"],
                        "keyword" : total_dict.word[i],
                        "word_type" : 0
                    }
                             )
            else:
                keyword.append(
                    {
                        "date" : news.loc[idx, "date"],
                        "keyword" : total_dict.word[i],
                        "word_type" : 1
                    }
                             )
    senti_score.append(sentiment)
dict = {
    "senti_score" : senti_score
}
senti = pd.DataFrame(dict)
news = pd.concat([news, senti], axis=1)
    
news.to_csv("./datas/pre/pre_news.csv", index=False)
keywords = pd.DataFrame(keyword)
keywords.to_csv("./datas/final/keywords.csv", index=False)


#SQL


    
    