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
                    # 1. JSONデータ（ラベル）を受信
                    json_data = await websocket1.recv()
                    await websocket.send_text(json_data)

                    # 2. 画像データを受信（バイナリデータ）
                    image_data = await websocket1.recv()
                    await websocket.send_bytes(image_data)

                except websockets.exceptions.ConnectionClosedError as e:
                    print(f"Connection closed with error: {e}")
                    break

    except WebSocketDisconnect:
        print("Client disconnected")

    finally:
        cap.release()  # カメラリソースを解放
