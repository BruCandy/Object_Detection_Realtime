from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from models.ssd_predictions import SSDPredictions
from models.ssd import SSD
import torch
import cv2
import numpy as np
import json


app = FastAPI()

voc_classes = ["kamukamu","tsubu"]

ssd_cfg = {
    'classes_num': 21,  # 背景クラスを含めた合計クラス数
    'input_size': 300,  # 画像の入力サイズ
    'dbox_num': [4, 6, 6, 6, 4, 4],  # 出力するDBoxのアスペクト比の種類
    'feature_maps': [38, 19, 10, 5, 3, 1],  # 各sourceの画像サイズ
    'steps': [8, 16, 32, 64, 100, 300],  # DBOXの大きさを決める
    'min_sizes': [30, 60, 111, 162, 213, 264],  # DBOXの大きさを決める
    'max_sizes': [60, 111, 162, 213, 264, 315],  # DBOXの大きさを決める
    'aspect_ratios': [[2], [2, 3], [2, 3], [2, 3], [2], [2]],
}

net = SSD(phase="test", cfg=ssd_cfg)
net_weights = torch.load(
    'api/models/グミ_weights_train.pth')

net.load_state_dict(net_weights)
net.to('cuda')

ssd = SSDPredictions(eval_categories=voc_classes, net=net)


@app.websocket("/ws")
async def detect_objects(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
                data = await websocket.receive_bytes()
    
                nparr = np.frombuffer(data, np.uint8)
                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                rgb_img, predict_bbox, pre_dict_label_index, scores = ssd.ssd_predict(image, confidence_threshold=0.8)

                drawn_image, labels = ssd.draw_on_image(rgb_img, predict_bbox, pre_dict_label_index, scores, voc_classes)

                await websocket.send_text(json.dumps({"labels": labels}))

                _, buffer = cv2.imencode('.jpg', drawn_image)
                await websocket.send_bytes(buffer.tobytes())
        
        except WebSocketDisconnect:
                break