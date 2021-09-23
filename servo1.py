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
#speed up button
button1 = Button(4)
#normalize button
button2 = Button(17)
#hours LED
led1 = LED(21)
#minutes LED
led2 = LED(26)
current = True
debouncer = 0
multiplier = 1
try:
    while True:
        if current:
            # get all the times and set them as ints
            # AKA we are not speeding up time
            seconds = int(datetime.now().strftime("%S"))
            tensminutes = minuter(int(datetime.now().strftime("%M")))
            onesminutes = int(datetime.now().strftime("%M"))%10
            hours = int(datetime.now().strftime("%H"))
            # unmilitarize the time
            if hours > 12:
                hours-=12
            # check if speed up button is pressed
            if button1.is_pressed:
                debouncer+=1
                if debouncer > 5:
                    current = False
                    multiplier+=1
                    debouncer = 0
            else:
                debouncer  = 0
                # constantly check if normalize button is being pressed while in sped up time
        elif button2.is_pressed:
            # go back to current time and reset multiplier
            current = True
            multiplier = 1
            debouncer = 0
        # if we are in time multiplying mode
        elif multiplier > 1:
            # check to speed time up faster
            if button1.is_pressed:
                debouncer += 1
                if debouncer > 5:
                    multiplier = multiplier * 2
                    debouncer = 0
            # reset time needed to press the button if released
            else:
                debouncer = 0
            # scale the seconds with the multiplier
            seconds = seconds + multiplier
            # basically just how a clock works 60 seconds add a 1 minute and reset seconds
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

        # all display code is useless but the display was very helpful in debugging so i left it in
        # print using lcd_display_string my apparent lack of time
        display.lcd_display_string("What time is it?",1)
        # print current seconds to LCD
        if seconds < 9:
            display.lcd_display_string(str(hours) + ":" + str(tensminutes) + str(onesminutes) + ":0" + str(seconds),2)
        else:
            display.lcd_display_string(str(hours) + ":" + str(tensminutes) +str(onesminutes) + ":" + str(seconds),2)
        # seconds LED active when odd and when time is sped up
        if multiplier > 1:
            led2.on()
        if seconds%2 == 1:
            led2.on()
        else:
            led2.off()
        # hours on when 10,11 or, 12 o clock
        if hours > 9:
            led1.on()
        else:
            led1.off()
        # set ones minute servo to 20 degree turn per minute passing because 9 holes to cover
        kit.servo[3].angle = 180 - ((onesminutes) * 20)
        # kit.servo[2].angle = seconds*3
        # set tens minute servo to 36 degree turn per minute passing because only 5 holes to cover
        kit.servo[1].angle = tensminutes*36
        # set hours servo 20 degree turn per minute passing because 9 holes to cover
        kit.servo[0].angle = 180 - ((hours%10) * 20)

# exit the loop on pressing ctrl+c
except KeyboardInterrupt:
    # clear the LCD display
    display.lcd_clear()
    # reset Servo angles to their respective 'zeros'
    kit.servo[0].angle = 180
    kit.servo[1].angle = 0
    kit.servo[3].angle = 180
    print("Exit")
    #clear the lcd
    display.lcd_clear()
