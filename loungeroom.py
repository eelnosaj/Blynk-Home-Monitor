import sched
import time as t
import sys
from datetime import date, time, datetime
import RPi.GPIO as GPIO
from astral import Astral

s = sched.scheduler(t.time, t.sleep)

GPIO.setmode(GPIO.BCM)
pin = 30  # GPIO pin connected to the PowerTail Switch II we want to control
GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

pwm = 18  # Backlight control pin for PiTFT PWM
GPIO.setup(pwm, GPIO.OUT, initial=GPIO.LOW)
backlight = GPIO.PWM(18, 1000)
backlight.start(50)


def relay_on():
    GPIO.output(pin, 1)  # Set pin high to activate the relay


def relay_off():
    GPIO.output(pin, 0)  # Set the pin low to deactivate the relay
    backlight.stop()
    GPIO.cleanup()
    sys.exit()

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
