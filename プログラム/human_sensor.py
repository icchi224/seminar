import RPi.GPIO as GPIO
from buildhat import Motor
import time

Human_Sensor = 14

GPIO.setmode(GPIO.BCM)
GPIO.setup(Human_Sensor, GPIO.IN)
motor_a = Motor('A')

try:
    print ('-----Start-----')
    n = 1
    while True:
        if GPIO.input(Human_Sensor) == GPIO.HIGH:
            motor_a.run_for_seconds(5)
            print("{}".format(n) + "回目検知")
            n += 1
            time.sleep(2)
        else:
            print(GPIO.input(Human_Sensor))
            time.sleep(2)
except KeyboardInterrupt:
    print("Cancel")
finally:
    GPIO.cleanup()
    print("-----end-----")