import asyncio
import json
import websockets
from collections import defaultdict

# Храним подключения по комнатам (group + student_id)
rooms = defaultdict(set)

async def handler(websocket, path):
    try:
        # При первом соединении клиент должен отправить { "room": "331-s04" }
        msg = await websocket.recv()
        data = json.loads(msg)
        room = data.get("room", "default")
        rooms[room].add(websocket)
        print(f"Client connected to room {room}. Total: {len(rooms[room])}")

        async for message in websocket:
            # Пересылаем сообщение всем в комнате, кроме отправителя
            for client in rooms[room]:
                if client != websocket:
                    await client.send(message)
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        if websocket in rooms[room]:
            rooms[room].remove(websocket)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("Signaling server running on ws://0.0.0.0:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())