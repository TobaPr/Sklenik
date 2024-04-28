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

GPIO.output(door_open_pin, False)
GPIO.output(door_close_pin, False)
GPIO.output(win_open_pin, False)
GPIO.output(win_close_pin, False)
GPIO.output(ventil_pin, False)
GPIO.output(fan_pin, False)

time.sleep(5)

try:
    while True:
        # ON
        GPIO.output(door_open_pin, GPIO.HIGH )
        print("Rele1 open")
        time.sleep(5)  # Počkáme 5 sekund
        
        GPIO.output(door_close_pin, GPIO.HIGH )
        print("Rele2 open")
        time.sleep(5)  # Počkáme 5 sekund

        GPIO.output(win_open_pin, GPIO.HIGH )
        print("Rele3 open")
        time.sleep(5)  # Počkáme 5 
        
        GPIO.output(win_close_pin, GPIO.HIGH )
        print("Rele4 open")
        time.sleep(5)  # Počkáme 5 sekund

        GPIO.output(ventil_pin, GPIO.HIGH )
        print("Rele7 open")
        time.sleep(5)  # Počkáme 5 sekund

        GPIO.output(fan_pin, GPIO.HIGH )
        print("Rele8 open")
        time.sleep(5)  # Počkáme 5 sekund



        # OFF
        GPIO.output(door_open_pin, GPIO.LOW)
        print("Rele1 open")
        time.sleep(5)  # Počkáme 5 sekund
        
        GPIO.output(door_close_pin, GPIO.LOW )
        print("Rele2 open")
        time.sleep(5)  # Počkáme 5 sekund

        GPIO.output(win_open_pin, GPIO.LOW )
        print("Rele3 open")
        time.sleep(5)  # Počkáme 5 
        
        GPIO.output(win_close_pin, GPIO.LOW )
        print("Rele4 open")
        time.sleep(5)  # Počkáme 5 sekund

        GPIO.output(ventil_pin, GPIO.LOW )
        print("Rele7 open")
        time.sleep(5)  # Počkáme 5 sekund

        GPIO.output(fan_pin, GPIO.LOW )
        print("Rele8 open")
        time.sleep(5)  # Počkáme 5 sekund


except KeyboardInterrupt:
    # Ukončení programu při stisknutí Ctrl+C
    GPIO.cleanup()