import numpy as np
import matplotlib.pyplot as plt 
import cv2  
import torch


from models.voc import DataTransform

#SSDモデルで物体検出を行うクラス
class SSDPredictions:
    def __init__(self, eval_categories, net):
        # クラス名のリストを取得
        self.eval_categories = eval_categories
        # SSDモデル
        self.net = net
        color_mean = (104, 117, 123)  # VOCデータの色の平均値(BGR)
        input_size = 300  # 画像の入力サイズは300×300
        # 前処理を行うDataTransformオブジェクトを生成
        self.transform = DataTransform(input_size, color_mean)

    #物体検出の予測結果を出力する
    def show(self, image_file_path, confidence_threshold):

        # SSDモデルで物体検出を行い、確信度が閾値以上のBBoxの情報を取得
        rgb_img, predict_bbox, pre_dict_label_index, scores = self.ssd_predict(
            image_file_path,      # 画像のファイルパス
            confidence_threshold) # 確信度の閾値
        
        # 検出結果を写真上に描画する
        self.draw(rgb_img,           # 画像のRGB値
                  bbox=predict_bbox, # 物体を検出したBBoxのリスト
                  label_index=pre_dict_label_index, # 物体のラベルへのインデックス
                  scores=scores,                    # 物体の確信度
                  label_names=self.eval_categories) # クラス名のリスト
    
    #SSDで物体検出を行い、確信度が高いBBoxの情報を返す
    def ssd_predict(self, image, confidence_threshold=0.5):
        # ［高さ］, ［幅］, ［RGB値］の要素数をカウントして画像のサイズとチャネル数を取得
        height, width, channels = image.shape
        # BGRからRGBへ変換
        rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # 画像の前処理
        phase = 'val'
        img_transformed, boxes, labels = self.transform(
            image,  # OpneCV2で読み込んだイメージデータ
            phase,# 'val'
            '',   # アノテーションは存在しない
            '') 
        # img_transformed(ndarray)の形状は(高さのピクセル数,幅のピクセル数,3)
        # 3はBGRの並びなのでこれをRGBの順に変更
        # (3, 高さのピクセル数, 幅のピクセル数)の形状の3階テンソルにする
        img = torch.from_numpy(
            img_transformed[:, :, (2, 1, 0)]).permute(2, 0, 1)
        
        img = img.to('cuda')

        # 学習済みSSDモデルで予測
        self.net.eval()  # ネットワークを推論モードにする
        """
        eval() メソッドは、PyTorchの nn.Module クラスにあらかじめ定義されており、
        そのメソッドをサブクラスで特別に定義しなくても自動的に使用できる。
        """
        x = img.unsqueeze(0)  # imgの形状をミニバッチの(1,3,300,300)にする
        # detections: 1枚の画像の各物体に対するBBoxの情報が格納される
        # (1, 21(クラス), 200(Top200のBBox), 5)
        # 最後の次元の5は[BBoxの確信度, xmin, ymin, width, height]
        detections = self.net(x)

        # confidence_threshold:
        predict_bbox = []
        pre_dict_label_index = []
        scores = []
        detections = detections.cpu().detach().numpy()

        # 予測結果から物体を検出したとする確信度の閾値以上のBBoxのインデックスを抽出
        # find_index(tuple): (［0次元のインデックス］,
        #                     ［1次元のインデックス],
        #                     [2次元のインデックス],
        #                     [3次元のインデックス],)
        #whereの出力はこのようになる
        #例 a = np.array([[1,2,3],[4,5,6],[7,8,9]])
        #np.where(a >= 5)
        #(array([1, 1, 2, 2, 2]), array([1, 2, 0, 1, 2]))
        #c = a[b]
        #array([5, 6, 7, 8, 9])
        find_index = np.where(detections[:, :, :, 0] >= confidence_threshold)
        
        # detections: (閾値以上のBBox数, 5)
        detections = detections[find_index]
        
        
        for i in range(len(find_index[1])):
            if (find_index[1][i]) > 0: # クラスのインデックス0以外に対して処理する
                sc = detections[i][0]  # detectionsから確信度を取得
                # BBoxの座標[xmin, ymin, width, height]のそれぞれと
                # 画像の[width, height, width, height]をかけ算する
                #モデルが出力する正規化された座標を実際の画像サイズに基づいたピクセル単位の座標に変換
                bbox = detections[i][1:] * [width, height, width, height]
                # find_indexのクラスの次元の値から-1する(背景0を引いて元の状態に戻す)
                lable_ind = find_index[1][i]-1

                # 確信度のリストに追加
                scores.append(sc)
                # BBoxのリストに追加
                predict_bbox.append(bbox)
                # 物体のラベルを追加
                pre_dict_label_index.append(lable_ind)

        
        # 1枚の画像のRGB値、BBox、物体のラベル、確信度を返す
        return rgb_img, predict_bbox, pre_dict_label_index, scores
    
    #物体検出の予測結果を写真上に描画する関数
    def draw_on_image(self, 
             rgb_img, #画像のRGB値
             bbox, #物体を検出したBBoxのリスト
             label_index, #物体のラベルへのインデックス
             scores, #物体の確信度
             label_names): #ラベル名の配列

        # クラスの数を取得
        num_classes = len(label_names)
        # BBoxの枠の色をクラスごとに設定
        colors = plt.cm.hsv(np.linspace(0, 1, num_classes)).tolist()

        # 画像を表示
        # plt.figure(figsize=(10, 10))
        # plt.imshow(rgb_img)
        # currentAxis = plt.gca()
        """
        gca()（Get Current Axis）関数は現在のアクシス（またはプロットエリア）
        のオブジェクトを返す。このアクシスオブジェクトを使用して、そのプロット
        エリアに対してさらなる描画操作（例えばバウンディングボックスの追加や
        テキストの描画）を行える。
        """

        labels = [] #変更点

        # 物体を検出したBBoxの数だけループ
        for i, bb in enumerate(bbox):
            # 予測した正解ラベルを取得
            label_name = label_names[label_index[i]]

            if label_name not in labels: #変更点
                labels.append(label_name)

            # ラベルに応じてBBoxの枠の色を変える
            # color = colors[label_index[i]]
            color = [int(c * 255) for c in colors[label_index[i]]]
            # 物体名と確信度をBBoxの枠上に表示する
            # 例：person：0.92　
            if scores is not None:
                sc = scores[i]
                display_txt = '%s: %.2f' % (label_name, sc)
            else:
                display_txt = '%s: ans' % (label_name)

            # BBoxの座標を取得
            # xy = (bb[0], bb[1])
            # width = bb[2] - bb[0]
            # height = bb[3] - bb[1]

            # BBoxを描画
            # currentAxis.add_patch(plt.Rectangle(
            #     xy,
            #     width,
            #     height,
            #     fill=False,
            #     edgecolor=color,
            #     linewidth=2)
            #     )

            # BBoxの枠の左上にラベルを描画
            # currentAxis.text(
            #     xy[0],
            #     xy[1],
            #     display_txt,
            #     bbox={'facecolor': color, 'alpha': 0.5}
            #     )

            bb = bb.astype(int)
            cv2.rectangle(rgb_img, (bb[0], bb[1]), (bb[2], bb[3]), color, 2)
            cv2.putText(rgb_img, display_txt, (bb[0], bb[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        return cv2.cvtColor(rgb_img, cv2.COLOR_RGB2BGR), labels     
"""
画像処理やコンピュータビジョンにおいて、バウンディングボックスの 
xminと y minを左上の角として定義するのは一般的な慣習。この慣習は
主に、画像のピクセル座標系が定義される方法に基づく。以下にその理由
と一般的な座標系について説明する。

画像の座標系
画像データにおいて、ピクセルの座標は通常、左上の角を原点として定義
される。x 軸は右方向に、y 軸は下方向に増加。つまり、画像の最初の
ピクセル（0,0)は左上に位置する。この座標系は、多くの画像処理ライブラリ
やコンピュータビジョンのフレームワークで採用されてる。

バウンディングボックスの定義
バウンディングボックスは、画像内の特定のオブジェクトを囲む最小の矩形
として定義される。通常、この矩形は以下の4つのパラメータによって定義
される。
x min:矩形の左端の x 座標。
y min:矩形の上端の y 座標。
幅（width:矩形の幅。
高さ（height):矩形の高さ。
ここで、x minと y minが左上の角を指すのは、それが座標系の始点に対応するため。
これにより、x minと幅を加算することで右端を、y minと高さを加算することで下端を
求めることができる。

利点
直感的理解：左上を起点とすることで、多くの人が紙の図や文書を見る際の自然な視覚的理解と一致。
実装の容易さ：座標と画像処理関数がこの標準に基づいているため、バウンディングボックスの計算や
操作が直接的で単純になる。
"""