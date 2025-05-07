import keras
import pandas as pd
from keras._tf_keras.keras.preprocessing.text import Tokenizer
from keras._tf_keras.keras.utils import pad_sequences

model = keras.models.load_model("./model/LSTM_NEWS.keras")

# print(model.summary())

news = pd.read_csv("./news_data.csv")
texts = news["title"].astype(str) + news["content"].astype(str)
tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
tokenizer.fit_on_texts(texts)
texts = tokenizer.texts_to_sequences(texts)
# print(texts)
texts = pad_sequences(texts, maxlen=100)
# print(texts)
pred = model.predict(texts)

pred_df = pd.DataFrame(pred)

pred_df = pd.concat([news["date"], pred_df], axis=1)
pred_df.to_csv("./datas/final/day_news_result.csv", index=False)