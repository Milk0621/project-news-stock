import asyncio
import websockets
import json
import pymysql

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
        #1. 미리 4시에 스케줄을 도는 함수를 만들어놓고 여기서 실행
        #2. 스케줄러가 돌고 난 뒤에 데이터베이스 인서트 -> finance_notification
        #2-2 매 2초마다 finance_notification 조회 -> #select * from finance_notification where flag = false
        #2-3 만약 false가 있으면 알림발송 후, true로 업데이트

        conn = pymysql.connect(
            host="158.247.211.92",
            user="milk",
            password="0621",
            database="kospi"
        )
        
        cursor = conn.cursor()
        sql = "select * from finance_notification where flag = false"
        cursor.execute(sql)

        result = cursor.fetchone()
        if result :
            title = result["title"]
            content = result["content"]
            #매일 오후 4시반에 인서트되는 내일 코스피 지수 예측 데이터 결과값 조회
            
            sql = "select id from user"
            cursor.execute(sql)
            ids = cursor.fetchall()
            title = [title] * len(ids)
            content = [content] * len(ids)
            #ids가 20명 -> 20개
            #유저테이블에있는 모든 유저의 아이디 조회

            sql = "insert into alarm(id, title, content, chekced)values(%s, %s, %s,False)"
            cursor.executemany(sql, (ids, title, content))
            conn.commit()

            #finance_notification의 flag를 True로 업데이트

        await asyncio.sleep(2)

        for connection in connected_clients:
            message = {
                "user" : "server",
                "type" : "stock",
                "message" : "서버에서보냄"
            }
            message =  json.dumps(message)
            await connection.send(message)


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
