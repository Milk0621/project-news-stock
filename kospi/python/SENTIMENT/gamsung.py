import pandas as pd
import re
from konlpy.tag import Okt

df = pd.read_csv("./datas/csv/pre_review.csv")

reviews = df[["review", "score"]]

stopwords = pd.read_csv("./datas/stopwords.txt")

okt = Okt()

print("리뷰 데이터 전처리 준비")

def preprocess(text):
    clean = re.sub(r"[^ㄱ-ㅎ가-힣0-9\s]", "", text)
    tokens = okt.morphs(clean, stem=True)
    filtered = [t for t in tokens if t not in stopwords]
    result = " ".join(filtered)
    return result

tokens = pd.DataFrame()
tokens = df["review"].astype(str).apply(preprocess)

print("리뷰 데이터 전처리")

word_dic = pd.read_csv("./datas/SentiWord_Dict.txt", delimiter="\t", header=None)
word_dic.rename(columns={0: 'word', 1: 'score'}, inplace=True)

print("감성 데이터 불러오기")
word_dic = word_dic.assign()

word_dic[["word", "score"]] = word_dic.str.split("\t", expand=True)

word_dic.to_csv("./datas/csv/pre_word_dic.csv", index=False)

for idx, token in enumerate(tokens):
    print(f"{idx}번 리뷰 데이터 처리")
    sentiment = 0
    for i in range(0, len(word_dic)):
        if word_dic.word[i] in token:
            sentiment += int(word_dic.score[i])
    reviews.loc[idx] = [token, sentiment]

reviews.to_csv("./datas/csv/gamsung.csv", index=False)

gamsung = pd.read_csv("./datas/csv/gamsung.csv")
review = pd.read_csv("./datas/csv/pre_review.csv")

gamsung = gamsung.rename(columns={"score" : "gamsung"})
gamsung = gamsung.drop(columns="review")

gamsung_review = pd.concat([review, gamsung], axis=1)

# gamsung_review.to_csv("./datas/csv/gamsung_review.csv")

gamsung_review = gamsung_review.drop(columns="score")
gamsung_review = gamsung_review.drop(columns="name")
gamsung_review = gamsung_review.drop(columns="review")

gamsung_score = gamsung_review.groupby("contentid").sum()

# gamsung_score.to_csv("./datas/csv/gamsung_score.csv")

pre_region = pd.read_csv("./datas/csv/pre_region_data2.csv")

pre_region = pre_region.drop(columns="total_score")

final_region = pd.merge(pre_region, gamsung_score, how="left", on="contentid")

final_region.to_csv("./datas/csv/final_region.csv", index=False)