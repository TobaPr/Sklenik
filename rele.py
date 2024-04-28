import RPi.GPIO as GPIO
import time

# Definujeme pin pro ovládání relé
door_open_pin = 5
door_close_pin = 6
win_open_pin = 13
win_close_pin = 19
ventil_pin = 16
fan_pin = 20

# Nastavíme režim pinu jako výstup
GPIO.setmode(GPIO.BCM)
GPIO.setup(door_open_pin, GPIO.OUT)
GPIO.setup(door_close_pin, GPIO.OUT)
GPIO.setup(win_open_pin, GPIO.OUT)
GPIO.setup(win_close_pin, GPIO.OUT)
GPIO.setup(ventil_pin, GPIO.OUT)
GPIO.setup(fan_pin, GPIO.OUT)



try:
    while True:
        # Dveře
        GPIO.output(door_close_pin, GPIO.LOW )
        GPIO.output(door_open_pin, GPIO.HIGH)
        print("Door open")
        time.sleep(5)  # Počkáme 5 sekund

        GPIO.output(door_open_pin, GPIO.LOW)
        GPIO.output(door_close_pin, GPIO.HIGH)
        print("Door close")
        time.sleep(5)  # Počkáme 5 sekund

        # Okno
        GPIO.output(win_close_pin, GPIO.LOW )
        GPIO.output(win_open_pin, GPIO.HIGH)
        print("Window open")
        time.sleep(5)  # Počkáme 5 sekund
        
        GPIO.output(win_open_pin, GPIO.LOW)
        GPIO.output(win_close_pin, GPIO.HIGH)
        print("Window close")
        time.sleep(5)  # Počkáme 5 sekund

        # Fan
        GPIO.output(fan_pin, GPIO.HIGH)
        print("Fan open")
        time.sleep(5) 
        GPIO.output(fan_pin, GPIO.LOW)
        print("Fan close")

        #ventil
        GPIO.output(ventil_pin, GPIO.HIGH)
        print("Ventil open")
        time.sleep(5) 
        GPIO.output(ventil_pin, GPIO.LOW)
        print("Ventil close")


except KeyboardInterrupt:
    # Ukončení programu při stisknutí Ctrl+C
    GPIO.cleanup()