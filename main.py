import websockets
import asyncio
import datetime
import random
import json


async def ws_server(websocket):
    print("WebSocket: Server Started.")
    try:
        i = 0
        while True:
            data = {
                "datetime": datetime.datetime.now().isoformat(),
                "location": {
                    "x": random.uniform(50, 51),
                    "y": random.uniform(22, 23),
                    "z": random.uniform(0, 50)
                },
                "velocity":random.uniform(10,20),
                "measurements": {
                    "20": random.uniform(-100, 0),
                    "30": random.uniform(-100, 0),
                    "40": random.uniform(-100, 0),
                    "50": random.uniform(-100, 0),
                    "60": random.uniform(-100, 0),
                    "70": random.uniform(-100, 0),
                    "80": random.uniform(-100, 0),
                    "90": random.uniform(-100, 0),
                    "100": random.uniform(-100, 0),
                    "110": random.uniform(-100, 0)
                }
            }
            json_data = json.dumps(data)
            await websocket.send(json_data)
            await asyncio.sleep(3)
    except websockets.ConnectionClosedError:
        print("Internal Server Error.")


async def main():
    async with websockets.serve(ws_server, "localhost", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())