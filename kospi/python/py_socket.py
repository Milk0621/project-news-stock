import asyncio
import websockets
import json

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
