import time
import os

print("USB_OFF")
a = 0
while a < 1000:
    os.system("sudo uhubctl -l 1-1 -a off")
    a += 1
    

print("USB_ON")
os.system("sudo uhubctl -l 1-1 -a on")