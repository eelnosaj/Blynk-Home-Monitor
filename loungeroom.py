import sched
import sys
import time as t
from datetime import date, time, datetime
import RPi.GPIO as GPIO
from astral import Astral

s = sched.scheduler(t.time, t.sleep)

def relay_on():
    GPIO.output(30, 1)  # Set pin high to activate the relay

def relay_off():
    GPIO.output(30, 0)  # Set the pin low to deactivate the relay
    backlight.ChangeDutyCycle(20)
    sys.exit()

def button1Pressed(channel):
        print("Button 1(23) pressed")

def button2Pressed(channel):
        print("Button 22 pressed")

def button3Pressed(channel):
        print("Button 27 pressed")

def button4Pressed(channel):
        print("Button 17 pressed")
        GPIO.output(30, not GPIO.input(30)) # Toggle GPIO output at pin 30 to activate/deactivate relay

GPIO.setmode(GPIO.BCM)
GPIO.setup(30, GPIO.OUT, initial=GPIO.LOW)         # GPIO pin connected to the PowerTail Switch II we want to control
GPIO.setup(18, GPIO.OUT)                           # Backlight control pin for PiTFT PWM
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 1
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 2 PiTFT
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 3 Buttons
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 4

GPIO.add_event_detect(23, GPIO.FALLING, callback=button1Pressed, bouncetime=2000)
GPIO.add_event_detect(22, GPIO.FALLING, callback=button2Pressed, bouncetime=2000)
GPIO.add_event_detect(27, GPIO.FALLING, callback=button3Pressed, bouncetime=2000)
GPIO.add_event_detect(17, GPIO.FALLING, callback=button4Pressed, bouncetime=2000)

backlight = GPIO.PWM(18, 1000)
backlight.start(100)

city_name = 'Sydney'  # City you want Astral to compute solar variables for
a = Astral()
a.solar_depression = 'civil'  # Civil, nautical or astronomical standard
city = a[city_name]

sun = city.sun(date=datetime.today(), local=True)  # Today's solar variables

sunset = sun['sunset']  # Store sunset time as a variable
timeon = sunset.timestamp()  # Convert to POSIX timestamp for scheduler

on = s.enterabs(timeon, 1, relay_on)  # Turn lamp on at sunset

bedtime = datetime.combine(date.today(), time(21, 30))
timeoff = bedtime.timestamp()

off = s.enterabs(timeoff, 1, relay_off)  # Turn lamp off at bedtime

s.run()
