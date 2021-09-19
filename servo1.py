import time
import drivers
from adafruit_servokit import ServoKit
from datetime import datetime

kit = ServoKit(channels=16)
display = drivers.Lcd()
try:
    while True:
        minute = int(datetime.now().strftime("%S"))
        print(minute)
        display.lcd_display_string("Not enough time",1)
        display.lcd_display_string(datetime.now().strftime("%S"),2)
        kit.servo[0].angle = minute*3
except KeyboardInterrupt:
    kit.servo[0].angle = 0
    print("Exit")
    display.lcd_clear()
