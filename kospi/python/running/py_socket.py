import asyncio
import websockets
import json
import pymysql
#import lstm_result_module
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from util.kiwoom import fn_ka20001, fn_au10001
#pip install websockets
# 연결된 클라이언트 목록
connected_clients = set()
#hong
#[hong]

async def handler(websocket):
    # 클라이언트 등록
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            #print(message["user"])
            
            json_message = json.loads(message)
            print(json_message["user"])
            
            print(message)
            for connection in connected_clients:
                if connection is not websocket:
                    await connection.send(message)
    except websockets.exceptions.ConnectionClosed:
        print("클라이언트 연결 종료")
    finally:
        connected_clients.remove(websocket)
        
async def test():
    try:
        ws_app = await websockets.connect("wss://api.kiwoom.com:10000/api/dostk/websocket",  ping_interval=None)
        param = {
            'trnm': 'LOGIN',
            'token': fn_au10001()
        }
        await ws_app.send(message=json.dumps(param))
        while True:
            response = json.loads(await ws_app.recv())
            if response.get('trnm') == 'LOGIN':
                if response.get('return_code') != 0:
                    print('로그인 실패하였습니다. : ', response.get('return_msg'))
                    await ws_app.close()
                else:
                    print('로그인 성공하였습니다.')
                    data = {
                        'trnm': 'REG', # 서비스명
                        'grp_no': '1', # 그룹번호
                        'refresh': '1', # 기존등록유지여부
                        'data': [{ # 실시간 등록 리스트
                            'item': ['001'], # 실시간 등록 요소
                            'type': ['0J'], # 실시간 항목
                        }]
                    }
                    await ws_app.send(message=json.dumps(data))
            elif response.get('trnm') == 'PING':
                await ws_app.send(json.dumps(response))

            if response.get('trnm') == 'REAL':
                print(f"결과아아아아아 {response}")
                conn = pymysql.connect(
                host="158.247.211.92",
                user="milk",
                password="0621",
                database="kospi"
                )
                cursor = conn.cursor()

                time = response['data'][0]['values']['20']
                price = response['data'][0]['values']['10']

                today = datetime.now()
                ymd = today.strftime("%Y-%m-%d")
                hour = time[:2]
                minute = time[2:4]
                second = time[4:]

                date_string = f"{ymd} {hour}:{minute}:{second}"
                date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
                price = price[1:]
                

                insert_query = """insert into chart(date, price) select %s, %s from dual where not exists
                (
                    select date from chart where date = %s
                )"""
                cursor.execute(insert_query, (date, price, date))
                conn.commit()
                    
            await asyncio.sleep(1)
    except websockets.exceptions.ConnectionClosedOK:
        ws_app = await websockets.connect("wss://api.kiwoom.com:10000/api/dostk/websocket",  ping_interval=None)
        
async def broadcast():
    while True:
        await asyncio.sleep(5)
        print("bloadcast works")
        #1. 미리 4시에 스케줄을 도는 함수를 만들어놓고 여기서 실행
        #2. 스케줄러가 돌고 난 뒤에 데이터베이스 인서트 -> finance_notification
        #2-2 매 2초마다 finance_notification 조회 -> #select * from finance_notification where flag = false
        #2-3 만약 false가 있으면 알림발송 후, true로 업데이트
        
        #lstm_result_module.job()

        conn = pymysql.connect(
            host="158.247.211.92",
            user="milk",
            password="0621",
            database="kospi",
            
        )

        cursor = conn.cursor()
        #(7, '내일 주가 알림', '내일 코스피 지수는 약 2542.011962890625 입니다.', 0)

        cursor = conn.cursor(pymysql.cursors.DictCursor)
        #{'no': 7, 'title': '내일 주가 알림', 'content': '내일 코스피 지수는 약 2542.011962890625 입니다.', 'flag': 0}
        sql = "select * from finance_notification where flag = 0"
        # print("flag=0 조회 완료")
        cursor.execute(sql)

        result = cursor.fetchone()
        if result :
            title = result["title"]
            content = result["content"]
            #매일 오후 4시반에 인서트되는 내일 코스피 지수 예측 데이터 결과값 조회
            
            sql = "select id from user where user_type != 99"
            cursor.execute(sql)
            ids = list(map(lambda x : x["id"] ,cursor.fetchall()))
            #[{'id': 'hong'}]
            #[{'id': 'hong'}, {"id" : "jeon"}]
            title = [title] * len(ids)
            #["내일 주가 알림"]
            
            content = [content] * len(ids)
            #["내일 코스피 지수는 약 ~~~ 입니다."]
            
            today = datetime.now()
            ymd = [today.strftime("%Y-%m-%d")] * len(ids)
            #['2025-04-28']
            
            data = list(zip(ids, title, content, ymd))
            #[('hong', '내일 주가 알림', '내일 코스피 지수는 약 2542.011962890625 입니다.', '2025-04-28')]
            
            #ids가 20명 -> 20개
            #유저테이블에있는 모든 유저의 아이디 조회

            sql = "insert into alarm(id, title, content, date)values(%s, %s, %s, %s)"
            cursor.executemany(sql, (data))
            conn.commit()

            #finance_notification의 flag를 True로 업데이트
            sql = "update finance_notification set flag = 1"
            cursor.execute(sql)
            conn.commit()
            
            
            for connection in connected_clients:
                message = {
                    "user" : "server",
                    "type" : "noti",
                    "message" : result["title"],
                    "content" : result["content"],
                    "date" : today.strftime("%Y-%m-%d")
                }
                message =  json.dumps(message)
                await connection.send(message)

        # print("알림발송 완료")

        # 3. API 실행
        #fn_ka20001(token=MY_ACCESS_TOKEN, data=params)
        #print()
        # for connection in connected_clients:
        #     message = {
        #         "user" : "server",
        #         "type" : "stock",
        #         "message" : result["title"]
        #     }
        #     message =  json.dumps(message)
        #     await connection.send(message)


        # await asyncio.sleep(10)  # 주기적 방송
        # msg = "[서버 메시지] 10초마다 전체 클라이언트에게 브로드캐스트"
        # print(f"서버 브로드캐스트: {msg}")
        # if connected_clients:
        #     await asyncio.wait([client.send(msg) for client in connected_clients])
        
        #SSE(Server Send Event)
        #Message Queue -> RabbitMq, Kafka
        #Websocket
        #dbEvent

async def main():
    asyncio.create_task(broadcast())
    asyncio.create_task(test())
    async with websockets.serve(handler, "localhost", 8765) as server :
        await server.serve_forever()

asyncio.run(main())
