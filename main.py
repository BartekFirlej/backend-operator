from flask import Flask, Response
import cv2, datetime, random, json, asyncio, threading, websockets

app = Flask(__name__)

def generate_frames():
    cap = cv2.VideoCapture("droneView.mp4")  # or your video source
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


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
                "velocity": random.uniform(10,20),
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


async def start_ws_server():
    async with websockets.serve(ws_server, "localhost", 8765):
        await asyncio.Future()  # run forever


def run_websocket_server():
    ws_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(ws_loop)
    ws_loop.run_until_complete(start_ws_server())


if __name__ == "__main__":
    ws_thread = threading.Thread(target=run_websocket_server)
    ws_thread.start()
    app.run(host="0.0.0.0", port=5000)