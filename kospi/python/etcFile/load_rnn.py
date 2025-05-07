import keras
import pandas as pd
from keras._tf_keras.keras.preprocessing.text import Tokenizer
from keras._tf_keras.keras.utils import pad_sequences

model = keras.models.load_model("./model/LSTM_NEWS.keras")

# print(model.summary())
texts = text = """
코스피가 장중 보합권에서 등락한 끝에 전 거래일 대비 5.00포인트(0.20%) 오른 2,488.42로 장을 마친 21일 오후 서울 중구 하나은행 딜링룸 현황판에 코스피 지수가 표시되고 있다.이날 코스닥 지수는 전 거래일보다 2.32포인트(0.32%) 내린 715.45로 마감했다.
"""
tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
tokenizer.fit_on_texts(texts)
texts = tokenizer.texts_to_sequences(texts)
# print(texts)
texts = pad_sequences(texts, maxlen=100)
# print(texts)
pred = model.predict(texts)

print(f"{pred}")

# pred_df = pd.DataFrame(pred)

# pred_df = pd.concat([news["date"], pred_df], axis=1)
# pred_df.to_csv("./datas/final/day_news_result.csv", index=False)