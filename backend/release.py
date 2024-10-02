import cv2

# カメラを開く
cap = cv2.VideoCapture(0)

# カメラが正しく開かれたかを確認
if cap.isOpened():
    print("カメラが解放されました")
    cap.release()  # カメラリソースを解放
else:
    print("カメラが見つかりませんでした")
