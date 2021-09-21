import time
#importing lcd drivers to drive the LCD board found from The_Raspberry_Pi_Guy Github
#https://github.com/the-raspberry-pi-guy/lcd
import drivers
#importing servokit to drive multiple servos using servodriver
from minuter import *
from adafruit_servokit import ServoKit
from gpiozero import LED, Button
#import time of day library
from datetime import datetime
#set number of servo channels
kit = ServoKit(channels=16)
#define the lcd drivers to be used
display = drivers.Lcd()
#led is on gpio pin 4
button1 = Button(4)
current = True
debouncer = 0
multiplier = 1
try:
    while True:
        if(current):
            #get the current #of seconds in the minute and set it as an integer
            #AKA we are not speeding up time
            seconds = int(datetime.now().strftime("%S"))
            tensminutes = minuter(int(datetime.now().strftime("%M")))
            onesminutes = int(datetime.now().strftime("%M"))
            hours = int(datetime.now().strftime("%H"))
            if(hours > 12):
                hours-=12
            if(button1.is_pressed):
                debouncer+=1
                print(debouncer)
                if(debouncer > 5):
                    current = False
            else:
                debouncer = 0
        else:
            seconds = seconds + multiplier

        #print using lcd_display_string my apparent lack of time
        display.lcd_display_string("What time is it?",1)
        #print current seconds
        display.lcd_display_string(str(hours) + ":" + str(tensminutes) +str(onesminutes) +  ":" + str(seconds),2)
        kit.servo[3].angle = (onesminutes%10) * 20
        kit.servo[2].angle = seconds*3
        kit.servo[1].angle = tensminutes*36
        kit.servo[0].angle = (hours%10) * 20

#exit the loop on pressing ctrl+c
except KeyboardInterrupt:
    #reset Servo angle
    kit.servo[0].angle = 0
    kit.servo[1].angle = 0
    kit.servo[2].angle = 0
    print("Exit")
    #clear the lcd
    display.lcd_clear()
