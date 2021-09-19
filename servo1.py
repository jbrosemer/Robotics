import time
#importing lcd drivers to drive the LCD board found from The_Raspberry_Pi_Guy Github
import drivers
#importing servokit to drive multiple servos using servodriver
from adafruit_servokit import ServoKit
#import time of day library
from datetime import datetime
#set number of servo channels
kit = ServoKit(channels=16)
#define the lcd drivers to be used
display = drivers.Lcd()
try:
    while True:
        #get the current #of seconds in the minute and set it as an integer
        seconds = int(datetime.now().strftime("%S"))
        #print using lcd_display_string my apparent lack of time
        display.lcd_display_string("Not enough time",1)
        #print current seconds
        display.lcd_display_string(datetime.now().strftime("%S"),2)
        kit.servo[0].angle = seconds*3
except KeyboardInterrupt:
    kit.servo[0].angle = 0
    print("Exit")
    display.lcd_clear()
