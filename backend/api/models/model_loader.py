import torch
from ssd import SSD #SSDクラスをインポート
from ssd_predictions import SSDPredictions

# VOC2012の正解ラベルのリスト
voc_classes = ["kamukamu","tsubu"]

# SSDモデルの設定値
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

# 推論モードのSSDモデルを生成
net = SSD(phase="test", cfg=ssd_cfg)
# 学習済みの重みを設定
net_weights = torch.load(
    './グミ_weights_train.pth',
    map_location={'cuda:0': 'cpu'})

# 重みをロードする
net.load_state_dict(net_weights)

# ファイルパス
image_file_path = "/content/drive/MyDrive/Colab Notebooks/その他/S__60596226.jpg"

# 予測と予測結果を画像で描画する
ssd = SSDPredictions(eval_categories=voc_classes, net=net)
# BBoxを抽出する際の閾値を0.6にする
ssd.show(image_file_path, confidence_threshold=0.9)