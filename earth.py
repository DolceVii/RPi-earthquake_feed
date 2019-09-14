#!/usr/bin/python3

import time
from RPi import GPIO
import Adafruit_CharLCD as LCD
import threading
from quakefeeds import QuakeFeed
import os

global Threadmemory
global Counter
Threadmemory = 0
Counter = 0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

lcd_rs        = 25  
lcd_en        = 24
lcd_d4        = 23
lcd_d5        = 17
lcd_d6        = 18
lcd_d7        = 22
lcd_backlight = 20

lcd_columns = 16
lcd_rows    = 2

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)
lcd.blink(False)
lcd.show_cursor(False)

lcd.set_backlight(0)
lcd.clear()

def earth_function():
    lcd.clear()
    global All
    global title
    global events
    global Threadmemory
    global Counter
    events = 0
    x = 0
    Threadmemory = 1
    while Threadmemory == 1:
        try:
            feed = QuakeFeed("2.5", "Day")
            M = str(feed.magnitude(events))
            All = str(feed.event_title(events))
            All = All[8:]
            x = All.find(",")
            Country = str(All[x+1:])
            if (Country == (" Greece")) :
                Counter = 1
                All = All[:x]
                title = ("M:" + M + " " + Country)
                events = 0
                lcd.set_backlight(0)
                print("M:" + M + " " + Country, All)
                os.system('mpg321 sound.mp3 &')
                time.sleep(60)
                os.system('clear')
                All = " "
                title = " "
                lcd.clear()
                Counter = 0
                
            elif (Counter == 0) :
                print("M:" + M + " " + All)
                All = " "
                title = " "
                lcd.set_backlight(1)
                events = events + 1
                lcd.set_cursor(0,0)
                lcd.message(" -= Search! =- ")
                lcd.set_cursor(0,1)
                lcd.message(" -= xXxXxXx =- ")
                Counter = 0
                time.sleep(1)
                lcd.clear()

        except IndexError:
            lcd.set_backlight(1)
            lcd.clear()
            lcd.set_cursor(0,0)
            lcd.message(" -= Nothing! =- ")
            lcd.set_cursor(0,1)
            lcd.message(" -= xxxxxxxx =- ")
            All = " "
            title = " "
            events = 0
            Counter = 0
            time.sleep(50)
            os.system('clear')

try:
    while True:
        while Counter == True  :
            len_msg = len(All) - (lcd_columns - 1)
            for i in range(len_msg):
                lcd.clear()
                lcd.message(title + "\n")
                lcd.message(All[i:i+lcd_columns] + "\n")
                time.sleep(0.5)
        
        if (Threadmemory == 0):
            Threadmemory = 1
            earth = threading.Thread(target = earth_function)
            earth.start()
            
        time.sleep(0.5)

except KeyboardInterrupt:
    lcd.clear()
    GPIO.cleanup()

finally:
    lcd.clear()
    GPIO.cleanup()
