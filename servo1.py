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
button1 = Button(4)
button2 = Button(17)
led1 = LED(18)
current = True
debouncer = 0
multiplier = 1
try:
    while True:
        if current:
            #get the current #of seconds in the minute and set it as an integer
            #AKA we are not speeding up time
            seconds = int(datetime.now().strftime("%S"))
            tensminutes = minuter(int(datetime.now().strftime("%M")))
            onesminutes = int(datetime.now().strftime("%M"))%10
            hours = int(datetime.now().strftime("%H"))
            if hours > 12:
                hours-=12
            if button1.is_pressed:
                debouncer+=1
                if debouncer > 5:
                    current = False
                    multiplier+=1
                    debouncer = 0
            else:
                debouncer = 0
        elif button2.is_pressed:
            current = True
            multiplier = 1
            debouncer = 0
        elif multiplier > 1:
            #onesminutes = onesminutes%10
            if button1.is_pressed:
                debouncer += 1
                if debouncer > 5:
                    multiplier = multiplier * 2
                    debouncer = 0
            else:
                debouncer = 0
            seconds = seconds + multiplier
            print(multiplier)
            print(onesminutes)
            if seconds > 59:
                seconds = 0
                if multiplier < 100:
                    onesminutes += 1
                elif multiplier > 100:
                    onesminutes += 2
                if onesminutes > 9:
                    onesminutes = 0
                    tensminutes += 1
                    if tensminutes > 5:
                        tensminutes = 0
                        hours += 1
                        if hours > 12:
                            hours -= 12


        #print using lcd_display_string my apparent lack of time
        display.lcd_display_string("What time is it?",1)
        #print current seconds
        if seconds < 9:
            display.lcd_display_string(str(hours) + ":" + str(tensminutes) + str(onesminutes) + ":0" + str(seconds),2)
        else:
            display.lcd_display_string(str(hours) + ":" + str(tensminutes) +str(onesminutes) + ":" + str(seconds),2)
        if seconds%2 == 1:
            led1.on()
        else:
            led1.off()
        kit.servo[3].angle = 180 - ((onesminutes) * 20)
        #kit.servo[2].angle = seconds*3
        kit.servo[1].angle = tensminutes*36
        kit.servo[0].angle = 180 - ((hours%10) * 20)

#exit the loop on pressing ctrl+c
except KeyboardInterrupt:
    display.lcd_clear()
    #reset Servo angle
    kit.servo[0].angle = 180
    kit.servo[1].angle = 0
    kit.servo[3].angle = 180
    print("Exit")
    #clear the lcd
    display.lcd_clear()
