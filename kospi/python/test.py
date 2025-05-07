# -*- coding: utf-8 -*-

from ML.kobert_finance import kobert_keyword

text = """
코스피가 장중 보합권에서 등락한 끝에 전 거래일 대비 5.00포인트(0.20%) 오른 2,488.42로 장을 마친 21일 오후 서울 중구 하나은행 딜링룸 현황판에 코스피 지수가 표시되고 있다.이날 코스닥 지수는 전 거래일보다 2.32포인트(0.32%) 내린 715.45로 마감했다.
"""

kobert_keyword(text)