#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import RPi.GPIO as GPIO
import os
import time
import random
import shlex
import subprocess
import smbus
from datetime import datetime
from buildhat import Motor
from __future__ import print_function
import nowtime
import speaker
from buildhat import Motor

# Pin Number
BOTTON_PIN = 19
LED_PIN = 25
motor_a = Motor('A')
GPIO.setmode(GPIO.BCM)
GPIO.setup(BOTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_PIN, GPIO.OUT)

# 学習済みモデルを読み込む
#faceCascade = cv2.CascadeClassifier('/home/sozo/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
faceCascade = cv2.CascadeClassifier('/home/sozo/opencv/data/haarcascades/haarcascade_eye.xml')

# カメラで動画を撮影する カメラ1台の場合は引数に0 or -1を設定する
cap = cv2.VideoCapture(0)
cap.set(3,640) # 横幅を設定 
cap.set(4,480) # 縦幅を設定

def main():
    last_pin_status = 0
    power_status = False
    nowtime.initialize() # 初期化
    while True:
        nowtime.get_time()
        pin_status = GPIO.input(BOTTON_PIN)

        # ボタンが押されたとき
        if (last_pin_status == 1 and pin_status == 0):
            if not power_status:
                # 電源ON
                song = speaker.play_song()  # 音楽ON
                GPIO.output(LED_PIN, GPIO.HIGH) # ライトON
                
                power_status = True

            else:
                #電源OFF
                speaker.stop_song(song) # 音楽OFF
                GPIO.output(LED_PIN, GPIO.LOW) # ライトOFF
                power_status = False

        last_pin_status = pin_status
        time.sleep(0.5)

def motor_ajust():
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
        time.sleep(0.1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # 例外処理(Ctrl+C)
        pass
    finally:
        # 終了時に行う処理
        LCD_BKL = 0x00 # バックライトOFF
        nowtime.send_data(0x01, 0) # LCD表示クリア
        GPIO.cleanup()
        speaker.stop_song()
        cap.release()
        cv2.destroyAllWindows()