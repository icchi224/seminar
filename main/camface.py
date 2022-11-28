import numpy as np
import cv2

# 学習済みモデルを読み込む
#faceCascade = cv2.CascadeClassifier('/home/sozo/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
faceCascade = cv2.CascadeClassifier('/home/sozo/opencv/data/haarcascades/haarcascade_eye.xml')

# カメラで動画を撮影する カメラ1台の場合は引数に0 or -1を設定する
cap = cv2.VideoCapture(0)
cap.set(3,640) # 横幅を設定 
cap.set(4,480) # 縦幅を設定
while True:

    # フレーム毎にキャプチャする
    ret, img = cap.read()

    # 顔検出の負荷軽減のために、キャプチャした画像をモノクロにする
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 顔検出のパラメータの設定
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,   
        minSize=(20, 20)
    )
    # 顔検出時に四角い枠を表示
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        print(x,y)

    # imshow関数で結果を表示する
    cv2.imshow('video',img)

    # ESCが押されたら終了する
    k = cv2.waitKey(30) & 0xff
    if k == 27: 
        break

cap.release()
cv2.destroyAllWindows()