# -*- coding: utf-8 -*- 
import pandas as pd
from konlpy.tag import Okt
import re

total_dict = pd.read_csv("./datas/dict/total_dict.csv")

news = pd.read_csv("./datas/origin/asia-2025-04-16.csv")

stopwords = pd.read_csv("./datas/dict/stopwords-ko.txt")

okt = Okt()

#전처리
def text_process(text):
    creaned = re.sub(r"[^ㄱ-ㅎ가-힣\s]", "", text)
    tokens = okt.morphs(creaned, stem=True)
    filtered = [t for t in tokens if t not in stopwords]
    result = " ".join(filtered)
    return result

# contents = news["content"]
# pre_news = [text_process(content) for content in contents]

# a = '''유가증권시장(코스피) 12월 결산 상장사들이 지난해 주주들에게 지급한 현금 배당금이 30조원을 돌파한 것으로 나타났다. 평균 시가배당률도 5년 만에 최고치를 달성했다. 16일 한국거래소에 따르면 코스피 12월 결산 807개 상장사 가운데 현금 배당을 실시한 기업은 565곳(70%)으로, 총 30조3451억원의 배당금을 지급한 것으로 조사됐다. 이는 2023년(27조4525억원) 대비 10%가량 늘어난 것으로 법인당 평균 배당금도 492억원에서 537억원으로 증가했다. 5년 이상 연속 배당을 실시한 법인은 454개사로 집계됐다. 한국거래소 서울 사무소의 모습. 특히 지난해 보통주와 우선주의 평균 시가배당률은 각각 3.05%, 3.70%로 모두 최근 5년 내 가장 높았다. 최근 5년간 업종별 평균 시가배당률은 금융(3.80%)이 가장 높았고 전기·가스(3.61%), 통신(3.49%)이 뒤를 이었다. 지난해 배당법인의 배당성향은 34.74%로 전년(34.31%) 대비 0.43%포인트 올랐다. 현금 배당을 실시한 법인은 지난해 주가가 평균 5.09% 하락했으나 같은 기간 코스피의 수익률(-9.63%) 대비 선방한 모습이다. 특히 밸류업(기업가치 제고) 참여 기업들의 배당실적이 두드러졌다. 밸류업 공시를 진행한 12월 결산법인 105곳 중 95%가 넘는 100곳이 배당을 실시한 가운데 이들 기업이 집행한 배당금은 총 18조원으로 코스피 현금 배당 총액의 59.2%를 차지했다. 지난해 밸류업 공시법인의 배당성향은 40.95%로 전체 현금배당 법인의 평균치를 상회한다. 거래소는 ""고금리, 환율 상승 등 경영환경 악화에도 불구하고 다수의 상장사가 기업이익의 주주환원 및 안정적인 배당정책 유지를 위해 노력하고 있는 것으로 본다""며 ""특히 밸류업 공시법인이 전체 배당법인과 비교해 더 높은 주주환원을 통해 기업가치 제고 및 국내 증시 활성화에 앞장서고 있음을 확인했다""고 설명했다. 한편 코스닥에서는 612개사가 총 2조3130억원의 현금배당을 지급했다. 배당법인 수는 2023년(607개사)보다 소폭 늘어 역대 최대를 기록했다. 배당금 규모 역시 전년(2조527억원) 대비 2603억원(12.7%) 늘었다. 5년 연속 결산배당을 실시한 법인은 402개사로 집계됐다. 코스닥 배당법인의 평균 배당성향은 34.4%로 최근 5년 내 최고치를 기록했다. 평균 시가배당률은 2.529%였다. 배당을 실시한 법인의 지난해 평균 주가 수익률은 -13.0%로, 같은 기간 코스닥 수익률(-21.7%) 대비 양호한 모습을 보였다.  <ⓒ투자가를 위한 경제콘텐츠 플랫폼, 아시아경제(www.asiae.co.kr) 무단전재 배포금지>'''

# a1 = text_process(a)
# dict = {
    
# }
# df = pd.DataFrame({
#     "content" : [""],
#     "score" : [""]
#     })
# df = df[["content", "score"]]
# print(df)

# # for idx, token in enumerate(a1):
# #     print(f"{idx}번 리뷰 데이터 처리")
# l = []
# sentiment = 0
# for i in range(0, len(total_dict)):
#     if total_dict.word[i] in a1:
#         sentiment += int(total_dict.score[i])
#     data = {
#         "content" : a1,
#         "score" : sentiment
#     }
#     l.append(data)
# l.to_csv("./datas/pre/test.csv")