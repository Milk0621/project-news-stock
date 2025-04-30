import pandas as pd
from keras._tf_keras.keras.preprocessing.text import Tokenizer
from keras._tf_keras.keras.utils import pad_sequences
import numpy as np
from keras import Sequential
from keras._tf_keras.keras.layers import Embedding, LSTM, Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import re

# 1. 데이터 로드
df = pd.read_csv("./datas/training/finance.csv").dropna(subset=["word", "labels"])

# 2. 텍스트 정제
def clean_text(text):
    return re.sub(r'[^ㄱ-ㅎ가-힣\s]', '', str(text)).strip()

texts = [clean_text(t) for t in df["word"].astype(str).tolist()]
labels = df["labels"].tolist()

# 3. 라벨 인코딩
y = LabelEncoder().fit_transform(labels)

# 4. 데이터 분할
from sklearn.model_selection import train_test_split
train_input, test_input, train_target, test_target = train_test_split(
    texts, y, test_size=0.2, random_state=42, stratify=y
)

# 5. 토크나이저 적용
tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
tokenizer.fit_on_texts(texts)
#오늘 금리는 -> [0,1]
#내일은 -> [2]
#오늘 : 0
#금리는 : 1
#문단의 길이가 15,000 -> 10,000으로 제한

train_input = tokenizer.texts_to_sequences(train_input)
test_input = tokenizer.texts_to_sequences(test_input)

train_input = pad_sequences(train_input, maxlen=200)
test_input = pad_sequences(test_input, maxlen=200)
#문자 -> 숫자 시퀀스로 변환된 텍스트 데이터의 길이를 200으로 맞춤
#[0, ~ 201] -> #[0 ~ 199]

print(train_input.shape)

model = Sequential()
model.add(Embedding(input_dim=10000, output_dim=32, input_length=200))
#숫자 시퀀스를 의미 벡터로 바꾸는 층 숫자 시퀀스 자체엔 의미 없음 → "7"은 'king'일 수도, 'banana'일 수도 → 각 숫자를 학습 가능한 밀집 벡터로 바꾸는 층
"""
input_dim=10000: 단어 사전 크기 (즉, 총 몇 개의 단어를 처리할 건가)

output_dim=32: 단어 하나를 몇 차원짜리 벡터로 바꿀 것인가 (의미를 담을 공간)

input_length=100: 입력 문장은 최대 몇 단어까지 받을 것인가 (패딩과 일치해야 함)
"""
model.add(LSTM(32))
model.add(Dense(3, activation='softmax'))
#0, 1, 2
#0 -> 긍정 / 1 -> 중립 / 2 -> 부정

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

print(model.summary())

model.fit(train_input, train_target, epochs=5, batch_size=64, validation_data=(test_input, test_target))

test_text = """
24일 코스피 지수가 외국인과 기관의 매도 공세 속에 소폭(0.1%) 하락세로 마감했다. 23일(현지시간) 미중 관세갈등 완화 기대감 속에 미국증시 3대 지수가 이틀째 급등했지만 한국증시는 좀처럼 힘을 내지 못했다. 이날 국내 대기업이 실적 발표 러시를 이룬 가운데 한국의 1분기 성장률이 마이너스(-)를 기록했다는 소식이 한국증시를 압박했다.

한국은행은 이날 1분기 실질 GDP(국내총생산)가 전기 대비 0.2%, 전년 동기 대비 0.1% 각각 감소했다고 발표했다. 이는 전월 전망치(0.2%)를 밑도는 수치로 2020년 코로나 이후 첫 역성장으로 평가된다. 또한 한국시간 이날 밤 시작되는 한미 관세협상 경계감도 지속된 가운데 일부 호실적주들에도 매도가 몰리는 모습을 보였다.

이날 원-달러 환율의 소폭 상승 속에 외국인들은 현선물시장에서 순매도에 나섰다. 외국인들의 현물 순매도는 10거래일 연속이다. 업종 및 테마별로는 태양광, 조선, 방산주 등이 올랐고 반도체, 2차전지, 자동차, 제약바이오, 철강주 등은 하락했다.

한국거래소에 따르면 SK하이닉스는 1분기 호실적 발표에도 1.49% 하락했다. 삼성전자는 등락 없이 5만5700원에 거래를 마쳤다.

태양광주 가운데 한화솔루션이 1분기 흑자전환을 발표한 가운데 주가도 13.15% 치솟았다.

조선주 중 HD한국조선해양과 삼성중공업이 1분기 실적 공개 속에 각각 6.85%, 2.03% 올랐고 HD현대중공업(2.45%), 한화오션(1.25%) 등도 상승했다. 방산주 중 한화에어로스페이스(1.23%), 한국항공우주(2.11%) 등이 상승했다.

건설주 중 GS건설(1.84%), DL이앤씨(1.47%), 현대건설(4.03%) 등이 상승했다. 화장품주 가운데 아모레퍼시픽(2.53%), 애경산업(1.49%) 등이 올랐다.

2차전지주들이 고개를 숙였다. LG에너지솔루션(-2.15%), 삼성SDI(-2.99%), 포스코퓨처엠(-1.96%) 등이 하락했다. 자동차주 가운데 현대차가 이날 1분기 실적 발표 속에 0.58% 하락했고 기아는 1.33% 내렸다.

IT 대형주 중 LG전자가 1분기 실적 발표 영향으로 1.40% 하락했다. 철강주 중 POSCO홀딩스가 1.15% 하락했다. 제약바이오주 가운데 삼성바이오로직스가 1분기 호실적 발표에도 1.88% 떨어졌다. 셀트리온은 0.81% 하락했다.

코스피 지수는 전일 대비 3.23포인트(0.13%) 하락한 2522.33을 기록했다. 개인이 1351억원을 순매수한 반면 외국인과 기관은 각각 78억원과 1986억원을 순매도했다. 거래량은 3억2372만주, 거래대금은 7조2185억원으로 집계됐다. 상·하한가 없이 404종목이 올랐고 458종목이 내렸다. 72종목은 보합이었다.

한편 코스닥 지수는 전일 대비 등락 없이 726.08로 마감했다.
""".strip().replace("\n", " ").replace("\r", "")

seq = tokenizer.texts_to_sequences([test_text])
    
# 길이 맞추기 (훈련 때 썼던 maxlen과 동일해야 함)
padded = pad_sequences(seq, maxlen=200)

# 예측
pred = model.predict(padded)

# 결과 해석
print(pred)
#2