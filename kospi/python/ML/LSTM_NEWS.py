# -*- coding: utf-8 -*-
import pandas as pd
from keras._tf_keras.keras.utils import pad_sequences
import numpy as np
import keras
from sklearn.model_selection import train_test_split
from keras._tf_keras.keras.preprocessing.text import Tokenizer

finance = pd.read_csv("./datas/training/finance.csv")

X = finance["word"].tolist()
y = finance["labels"].tolist()

train_input, test_input, train_target, test_target = train_test_split(X,y, test_size=0.2, stratify=y)

#훈련데이터, 테스트데이터

#학습 -> 훈련데이터 -> 훈련 / 검증
#테스트, 검증 -> 테스트데이터

#전처리
tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")

tokenizer.fit_on_texts(train_input)
#train_input = 안녕하세요 저는 홍길동 입니다.
#안녕하세요
#->[0, 1, 2, 3],[0]


train_input = tokenizer.texts_to_sequences(train_input)
test_input = tokenizer.texts_to_sequences(test_input)

train_input = pad_sequences(train_input, maxlen=100)
test_input = pad_sequences(test_input, maxlen=100)

train_target = np.array(train_target)
test_target = np.array(test_target)

model = keras.Sequential()
embedding = keras.layers.Embedding(input_dim=10000, output_dim=32)

rnn = keras.layers.LSTM(32)

#은닉층
dense = keras.layers.Dense(50, activation="relu")

#드롭아웃
dropout = keras.layers.Dropout(0.2)

output = keras.layers.Dense(3, activation="softmax")

model.add(embedding)
model.add(rnn)
model.add(dense)
model.add(dropout)
model.add(output)
model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
#0, 1, 2 -> 0 0 1 / 0 1 0 / 0 1 1

early_stop_cb = keras.callbacks.EarlyStopping(patience=2, restore_best_weights=True)

history = model.fit(train_input, train_target, epochs=50, batch_size=64, validation_data=(test_input, test_target), callbacks=[early_stop_cb], verbose=1)

model.save("./model/LSTM_NEWS.keras")

# new_text = """설 황금연휴를 거쳐 반등을 모색해온 LCC(저비용항공사) 등 항공관련주가 또 한번의 악재를 맞았다.참사 한달여만에화재 사고로 항공기 이용 불안심리가 커진 영향으로 분석된다.지난달 31일 한국거래소에 따르면 코스피 상장사 에어부산은 이날 2395원에 거래가 마감됐다. 전 거래일인 1월 24일 대비 3.23% 하락했다. 에어부산 외에도(-2.91%), 제주항공(-0.94%),(-1.09%) 등 LCC 관련주가 모두 하락세로 마감했다. 경영권 분쟁으로 급등했던과도 각각 5.11%, 5.54% 급락했다. 대형항공사를 제외한 대부분의 LCC가 설 연휴가 끝나기 무섭게 하락세로 돌아선 것이다.항공기업의 주가 약세는 지난달 28일 부산 김해공항에서 홍콩으로 가려던 에어부산 BX391편에서 화재가 발생한 영향이다. 항공기 동체 상부를 태운 불은 인명피해 없이 전소됐지만 거듭된 항공기 사고로 인해 승객의 불안심리는 한층 가중됐다. 인명사고가 없고 화재사고 원인이 기내에 반입된 휴대용 배터리에서 발생한 것으로 예측되면서 가격 하락폭은 제한적이었다. 그러나 이륙 후 같은 상황이 발생한다면 더 큰 피해가 발생할 수 있어 해소되지 않은 리스크라는 지적도 있다.지난해 항공관련주는 티메프(티몬·위메프) 미정산 사태로 부진을 면치 못하다 원/달러 환율 급등까지 겹치면서 연말 대목에도 하락세를 이어갔다. 환율 급등은 해외여행 수요 위축을 불러올 뿐 아니라 달러로 지불하는 항공기 리스비와 유류비 인상도 초래해 항공주에 악재다.여기에 제주항공 참사까지 발생하면서 연초까지 저공비행이 이어졌다. 인천국제공항 출국 보안검색 규정강화와 심사인원 부족 문제도 해외여행을 꺼리는 심리를 부채질 했다. 그나마 대체공휴일 지정으로 설 연휴기간 105만명이 해외에 출국하는 역대 최다 기록을 세운 영향으로 주가는 바닥을 찍는듯 했다. 하지만 거듭된 항공기 사고로 소비자 불안심리가 주가에 반영되는 모습이다. 지난해 12월29일 179명의 사망자를 낸 제주항공 참사가 발생한지 불과 한 달만에 벌어진 사고다. 전날 미국 워싱턴DC에서 발생한 항공기와 헬기 충돌사고까지 발생하면서 이런 심리는 가중됐다.증권업계도 항공주의 단기적 회복은 어렵다는 판단이다. 최고운 한국투자증권 애널리스트는 ""항공기 안전 문제와 소비자 불안은 어느 항공사나 자유롭지 못하다""며 ""정확한 사고원인을 규명하려면 최소 6개월에서 1년이 걸리지만 사회적 불안감 해소는 이보다 더 긴 시간이 걸릴 수 있다""고 평가했다."""

# texts = tokenizer.texts_to_sequences([new_text])
# print(texts)
# texts = pad_sequences(texts, maxlen=100)
# print(texts)

# pred = model.predict(texts)
# print(pred)