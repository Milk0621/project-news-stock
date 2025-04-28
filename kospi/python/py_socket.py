import asyncio
import websockets
import json
import pymysql
#import lstm_result_module
import datetime
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
            
            for connection in connected_clients:
                if connection is not websocket:
                    await connection.send(message)
    except websockets.exceptions.ConnectionClosed:
        print("클라이언트 연결 종료")
    finally:
        connected_clients.remove(websocket)
async def broadcast():
    while True:
        await asyncio.sleep(5)
        #1. 미리 4시에 스케줄을 도는 함수를 만들어놓고 여기서 실행
        #2. 스케줄러가 돌고 난 뒤에 데이터베이스 인서트 -> finance_notification
        #2-2 매 2초마다 finance_notification 조회 -> #select * from finance_notification where flag = false
        #2-3 만약 false가 있으면 알림발송 후, true로 업데이트
        
        #lstm_result_module.job()
        print("분석완료!")

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
        print("flag=0 조회 완료")
        cursor.execute(sql)

        result = cursor.fetchone()
        print(result)
        if result :
            print("결과 있음")
            title = result["title"]
            content = result["content"]
            #매일 오후 4시반에 인서트되는 내일 코스피 지수 예측 데이터 결과값 조회
            
            sql = "select id from user where user_type != 99"
            print("회원 조회 완료")
            cursor.execute(sql)
            ids = list(map(lambda x : x["id"] ,cursor.fetchall()))
            #[{'id': 'hong'}]
            #[{'id': 'hong'}, {"id" : "jeon"}]
            print(ids)
            title = [title] * len(ids)
            #["내일 주가 알림"]
            
            content = [content] * len(ids)
            #["내일 코스피 지수는 약 ~~~ 입니다."]
            
            today = datetime.datetime.now()
            ymd = [today.strftime("%Y-%m-%d")] * len(ids)
            #['2025-04-28']
            
            data = list(zip(ids, title, content, ymd))
            #[('hong', '내일 주가 알림', '내일 코스피 지수는 약 2542.011962890625 입니다.', '2025-04-28')]
            
            print(ymd)
            #ids가 20명 -> 20개
            #유저테이블에있는 모든 유저의 아이디 조회

            sql = "insert into alarm(id, title, content, date)values(%s, %s, %s, %s)"
            cursor.executemany(sql, (data))
            conn.commit()

            #finance_notification의 flag를 True로 업데이트
            sql = "update finance_notification set flag = 1"
            cursor.execute(sql)
            conn.commit()
            print("flag 1로 업데이트 완료")
            
            for connection in connected_clients:
                message = {
                    "user" : "server",
                    "type" : "noti",
                    "message" : result["title"]
                }
                message =  json.dumps(message)
                await connection.send(message)

        # print("알림발송 완료")

        


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
    async with websockets.serve(handler, "localhost", 8765) as server :
        await server.serve_forever()

asyncio.run(main())
