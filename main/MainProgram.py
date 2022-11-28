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

# Pin Number
BOTTON_PIN = 19
LED_PIN = 25
GPIO.setmode(GPIO.BCM)
GPIO.setup(BOTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_PIN, GPIO.OUT)

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