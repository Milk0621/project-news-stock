import tensorflow as tf
import numpy as np
from transformers import BertTokenizer, TFBertForSequenceClassification
from collections import defaultdict

def kobert_keyword(text):
    # 경로
    MODEL_PATH = "./tf_kor_finbert"

    # 토크나이저 및 모델 로드
    tokenizer = BertTokenizer.from_pretrained(MODEL_PATH)
    #사전학습된 토크나이저 불러오기

    model = TFBertForSequenceClassification.from_pretrained(MODEL_PATH, output_attentions=True)
    #사전학습된 모델 불러오기

    text = text.replace("\n", " ").replace("\r", "").strip()

    # 토큰화
    inputs = tokenizer(
        text,
        return_tensors="tf",
        max_length=512,
        truncation=True,
        padding="max_length"
    )

    print(inputs)

    # 예측 수행 (training=False 필수)
    outputs = model(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        token_type_ids=inputs["token_type_ids"],
        training=False
    )

    print(outputs)

    # 확률 계산 및 예측 클래스
    probs = tf.nn.softmax(outputs.logits, axis=-1).numpy()[0]
    np.set_printoptions(suppress=True)
    percentages = probs * 100
    percentages_rounded = np.round(percentages, 2)
    #[0.1, 0.5, 0.4]
    pred_class = np.argmax(probs)
    print(percentages_rounded)
    #1


    label_map = {0: "부정", 1: "중립", 2: "긍정"}
    print(f"\n[예측 결과] → {label_map[pred_class]} ")
    senti_result = label_map[pred_class]
    
    # print(f"[클래스별 확률] → {probs}")

    # 어텐션 출력 (키워드 부분)
    attentions = outputs.attentions
    last_layer = attentions[-1][0].numpy()  # shape: (num_heads, seq_len, seq_len)
    mean_attention = np.mean(np.sum(last_layer, axis=1), axis=0)  # shape: (seq_len,)
    
    # 토큰 시각화
    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0].numpy())
    def merge_wordpieces(tokens, scores):
        merged_tokens = []
        merged_scores = []
        current_word = ""
        current_score = 0.0
        count = 0

        for token, score in zip(tokens, scores):
            if token in ["[PAD]", "[CLS]", "[SEP]"]:
                continue

            if token.startswith("##"):
                current_word += token[2:]
            else:
                if current_word:
                    merged_tokens.append(current_word)
                    merged_scores.append(current_score / max(count, 1))
                current_word = token
                current_score = 0.0
                count = 0

            current_score += score
            count += 1

        if current_word:
            merged_tokens.append(current_word)
            merged_scores.append(current_score / max(count, 1))

        return merged_tokens, merged_scores

    merged_tokens, merged_scores = merge_wordpieces(tokens, mean_attention)
    
    top_n = 10
    top_indices = np.argsort(merged_scores)[-top_n:][::-1]

    postpositions = ["을", "를", "에", "의", "는", "가", "이", "은", "와", "과", "에서", "에게", "께"]

    def clean_token(token):
        for josa in postpositions:
            if token.endswith(josa):
                return token[:-len(josa)]
        return token

    filtered_results = [
        (clean_token(merged_tokens[i]), merged_scores[i])
        for i in top_indices
        if merged_tokens[i].isalpha()
    ]
    
    agg_scores = defaultdict(list)
    for token, score in filtered_results:
        agg_scores[token].append(score)

    final_top = sorted(
        [(token, np.mean(scores)) for token, scores in agg_scores.items()],
        key=lambda x: x[1], reverse=True
    )[:5]
    
    print("\n[후처리된 단어 기준 어텐션 상위 10개]")
    keyword = []
    for token, score in final_top:
        print(f"{token} (평균 가중치: {score:.4f})")
        keyword.append(token)

    return senti_result, keyword, percentages_rounded

#csv 데이터를 이용한 검증
# import pandas as pd
# from sklearn.preprocessing import LabelEncoder
# from sklearn.metrics import classification_report
# from tqdm import tqdm

# # CSV 데이터 로드 및 전처리
# df = pd.read_csv("./dl/finance_data.csv").dropna(subset=["kor_sentence", "labels"])
# texts = df["kor_sentence"].astype(str).tolist()
# labels = df["labels"].tolist()

# # 라벨 인코딩
# label_encoder = LabelEncoder()
# y_true = label_encoder.fit_transform(labels)

# # 추론을 위한 배치 처리
# BATCH_SIZE = 32
# MAX_LEN = 128
# y_pred = []

# for i in tqdm(range(0, len(texts), BATCH_SIZE)):
#     batch_texts = texts[i:i + BATCH_SIZE]
#     encodings = tokenizer(
#         batch_texts,
#         return_tensors="tf",
#         padding="max_length",
#         truncation=True,
#         max_length=MAX_LEN
#     )
#     outputs = loaded_model({
#         "input_ids": encodings["input_ids"],
#         "attention_mask": encodings["attention_mask"],
#         "token_type_ids": encodings["token_type_ids"]
#     })
#     probs = tf.nn.softmax(outputs["logits"], axis=-1).numpy()
#     preds = np.argmax(probs, axis=1)
#     y_pred.extend(preds)

# # 성능 측정
# print("\n[CSV 전체 데이터 평가 결과]")
# print(classification_report(y_true, y_pred, target_names=label_encoder.classes_, digits=4))

