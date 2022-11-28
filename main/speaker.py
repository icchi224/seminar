# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 10:40:49 2022

@author: sd20022
"""

#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

import RPi.GPIO as GPIO
import os
import time
import random
import shlex
import subprocess

# Pin Number
PIN = 19

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
last_pin_status = 0
song = False
p = 0




def play_song():
    SONG_DIR = '/home/sozo/音楽/'
    SONG_LIST = ['昼下がり気分.mp3','高原の小さなカフェにて.mp3','HIRAHIRA.mp3']
    song = random.choice(SONG_LIST)
    song_path = os.path.join(SONG_DIR, song)
    command = 'mpg321 %s' % (song_path)
    p = subprocess.Popen(shlex.split(command))
    return p

def stop_song(p) :
    p.kill()

def main():
    while True:
        pin_status = GPIO.input(PIN)
        if last_pin_status == 1 and pin_status == 0:
            if not song:
                p = play_song()
                song = True
            else:
                stop_song(p)
                song = False

        last_pin_status = pin_status
        time.sleep(0.1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # 例外処理(Ctrl+C)
        pass
    finally:
        GPIO.cleanup()
        stop_song()
