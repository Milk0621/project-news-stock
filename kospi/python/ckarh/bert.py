from transformers import pipeline

model_name='snunlp/KR-FinBert-SC'
ko_finbert = pipeline(task='text-classification', model=model_name)

# text 생성
# text = """
# 오르락 내리락 적당히 유지중인 코스피는 2,500선을 지키고 있다.
# """.replace("\n", " ").replace("\r", "").strip()
#중립

text = """
국제 전자산업 회사인 엘코텍은 탈린 공장에서 수십 명의 직원을 해고했으며, 이전의 해고와는 달리 회사는 사무직 직원 수를 줄였다고 일간 포스티메스가 보도했다.
""".replace("\n", " ").replace("\r", "").strip()
#부정

# 감성 분석 실행
result = ko_finbert(text)

# 결과 확인하기
print(result)