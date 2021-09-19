import time
import drivers
from adafruit_servokit import ServoKit
from datetime import datetime

kit = ServoKit(channels=16)
display = drivers.Lcd()
try:
    while True:
        display.lcd_display_string("Not enough time",1)
        display.lcd_display_string(datetime.now().strftime("%M"),2)
        kit.servo[0].angle = 180
        time.sleep(1)
        kit.servo[0].angle = 0
        time.sleep(1)
except KeyboardInterrupt:
    print("Exit")
    
