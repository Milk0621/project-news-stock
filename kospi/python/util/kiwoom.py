import pandas as pd
import requests
import json
from dotenv import load_dotenv
load_dotenv()
import os
import time as t

# 접근토큰 발급
def fn_au10001():
    # 1. 요청할 API URL
    #host = 'https://mockapi.kiwoom.com' # 모의투자
    host = 'https://api.kiwoom.com' # 실전투자
    endpoint = '/oauth2/token'
    url =  host + endpoint

    # 2. header 데이터
    headers = {
        'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
    }
    appkey = os.getenv("appkey")
    secretkey = os.getenv("secretkey")
    
    data = {
        'grant_type': 'client_credentials',  # grant_type
        'appkey': appkey,  # 앱키
        'secretkey': secretkey,  # 시크릿키
    }

    # 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    token = result.get("token")
    return token
    
	# 4. 응답 상태 코드와 데이터 출력
	# print('Code:', response.status_code)
	# print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
	# print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))  # JSON 응답을 파싱하여 출력
    
    # 실행 구간
# if __name__ == '__main__':
# 	# 2. API 실행
#     fn_au10001()



# 업종현재가요청
def fn_ka20001(token, cont_yn='N', next_key=''):
	# 1. 요청할 API URL
	#host = 'https://mockapi.kiwoom.com' # 모의투자
    host = 'https://api.kiwoom.com' # 실전투자
    endpoint = '/api/dostk/sect'
    url =  host + endpoint
    
    data = {
        'mrkt_tp': '0', # 시장구분 0:코스피, 1:코스닥, 2:코스피200
        'inds_cd': '001', # 업종코드 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주 101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100 나머지 ※ 업종코드 참고
    }

    # 2. header 데이터
    headers = {
        'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
        'authorization': f'Bearer {token}', # 접근토큰
        'cont-yn': cont_yn, # 연속조회여부
        'next-key': next_key, # 연속조회키
        'api-id': 'ka20001' # TR명
    }
    
    # 3. http POST 요청
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    print(result)
    if response.headers["cont-yn"] == "Y":
        key = response.headers["next-key"]
        t.sleep(1)
        fn_ka20001(token=token, cont_yn = "Y", next_key = key)
    else:
        pass
    
    price = result["inds_cur_prc_tm"][0]["cur_prc_n"]
    time = result["inds_cur_prc_tm"][0]["tm_n"]
    # hour = time[:2]
    # minute = time[2:4]
	# 4. 응답 상태 코드와 데이터 출력
	# print('Code:', response.status_code)
	# print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
	# print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))  # JSON 응답을 파싱하여 출력
    return price, time
 

# 실행 구간
if __name__ == '__main__':
    # 1. 토큰 설정
    #MY_ACCESS_TOKEN = 'xRFWRkLY2hU_TB4sGBhbGICuIYFzdz65TZgW4yqeQp_xWLKyeMUSlLZyPE-bWEJTVEVJmpTRUvniuLV3OQZesg'# 접근토큰

    # 2. 요청 데이터
    # params = {
    #     'mrkt_tp': '0', # 시장구분 0:코스피, 1:코스닥, 2:코스피200
    #     'inds_cd': '001', # 업종코드 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주 101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100 나머지 ※ 업종코드 참고
    # }
 
    token = fn_au10001()
    #print(token)

    # 3. API 실행
    price, time = fn_ka20001(token=token)
    print(price, time)
	# next-key, cont-yn 값이 있을 경우
	# fn_ka20001(token=MY_ACCESS_TOKEN, data=params, cont_yn='Y', next_key='nextkey..'