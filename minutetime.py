import drivers
from time import sleep
from datetime import datetime

display = drivers.Lcd()

try:
    while True:
        display.lcd_display_string("Not enough time",1)
        display.lcd_display_string(datetime.now().strftime("%H"),2)
    
except KeyboardInterrupt:
    print("Terminated")
    display.lcd_clear()
    