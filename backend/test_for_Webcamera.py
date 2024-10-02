import cv2
import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import websockets

app = FastAPI()

url2 = "ws://localhost:8000/ws"

@app.websocket("/ws")
async def detect_objects(websocket: WebSocket):
    await websocket.accept()

    cap = cv2.VideoCapture(0)

    try:
        async with websockets.connect(url2) as websocket1:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # フレームをJPEG形式でエンコード
                _, img_encoded = cv2.imencode('.jpg', frame)

                # WebSocketでサーバーに画像を送信
                await websocket1.send(img_encoded.tobytes())

                # サーバーからの応答を受信（物体検出結果画像）
                try:
                    data = await websocket1.recv()
                except websockets.exceptions.ConnectionClosedError as e:
                    print(f"Connection closed with error: {e}")
                    break

                # クライアントへ物体検出結果を送信
                await websocket.send_bytes(data)

    except WebSocketDisconnect:
        print("Client disconnected")

    finally:
        cap.release()  # カメラリソースを解放
