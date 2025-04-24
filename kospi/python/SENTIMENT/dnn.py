import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import keras
import matplotlib.pyplot as plt

label_dict = pd.read_csv("./datas/dict/total_dict.csv")
sentiment_dict = dict(zip(label_dict["word"], label_dict["score"]))

def sentiment_label(text):
    tokens = str(text).split()
    score = sum(sentiment_dict.get(token, 0) for token in tokens)
    if score > 0:
        return 1
    elif score < 0:
        return -1
    else:
        return 0
    
news_data = pd.read_csv("news_data.csv")
news_data["sentiment"] = news_data["content"].apply(sentiment_label)

# print(news_data)

content = news_data["content"].fillna("")
label = news_data["sentiment"].map({-1:0, 0:1, 1:2}).values.reshape(-1, 1)

# print(content)
# print(label)

vectorizer = TfidfVectorizer(max_features=7000, ngram_range=(1, 2))
X = vectorizer.fit_transform(content).toarray()

encoder = OneHotEncoder(sparse_output=False)
y = encoder.fit_transform(label)

train_input, test_input, train_target, test_target = train_test_split(X, y, test_size=0.2, stratify=y)

dense1 = keras.layers.Dense(256, activation="relu", input_shape=(X.shape[1],))
dense2 = keras.layers.Dense(128, activation="relu")
dense3 = keras.layers.Dense(64, activation="relu")
dropout = keras.layers.Dropout(0.3)
output = keras.layers.Dense(3, activation="softmax")

model = keras.Sequential([dense1, dense2, dense3, dropout, output])

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
print(model.summary())

early_stop_cb = keras.callbacks.EarlyStopping(patience=2, restore_best_weights=True)

history = model.fit(train_input, train_target, epochs=100, batch_size=32, validation_split=0.2, callbacks=[early_stop_cb])
loss, acc = model.evaluate(test_input, test_target)
print(loss, acc)

test_sentences = [
    "코스피가 급락하며 투자자들의 불안감이 커지고 있다.",
    "삼성전자가 분기 최대 실적을 기록했다.",
    "금리 동결 소식에 시장은 잠잠한 반응을 보이고 있다."
]

# TF-IDF 벡터화
test_vectors = vectorizer.transform(test_sentences).toarray()

# 예측 실행
predictions = model.predict(test_vectors)
predicted_classes = predictions.argmax(axis=1)  # 확률이 가장 높은 클래스 선택

# 감성 라벨 맵
label_map = {0: "부정", 1: "중립", 2: "긍정"}

# 결과 출력
for sentence, pred in zip(test_sentences, predicted_classes):
    print(f"{sentence}\n 예측 감성: {label_map[pred]}\n")