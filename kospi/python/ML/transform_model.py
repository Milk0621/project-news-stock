# PyTorch → TensorFlow 변환 수행 (환경에 transformers 설치되어야 작동)
from transformers import TFBertForSequenceClassification, BertConfig, BertTokenizer, BertForSequenceClassification

# 모델명
model_name = "snunlp/KR-FinBERT-SC"

# PyTorch 모델 로드 및 구성
torch_model = BertForSequenceClassification.from_pretrained(model_name)
config = BertConfig.from_pretrained(model_name)
tokenizer = BertTokenizer.from_pretrained(model_name)

# TensorFlow용 모델로 변환
tf_model = TFBertForSequenceClassification.from_pretrained(model_name, from_pt=True)

# 저장 (TensorFlow용)
tf_model.save_pretrained("./tf_kor_finbert")
tokenizer.save_pretrained("./tf_kor_finbert")
