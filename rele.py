import RPi.GPIO as GPIO
import time

# Definujeme pin pro ovládání relé
relay_pin = 19

# Nastavíme režim pinu jako výstup
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin, GPIO.OUT)

try:
    while True:
        # Zapneme relé (nastavíme pin na HIGH)
        GPIO.output(relay_pin, GPIO.HIGH)
        print("Relay ON")
        time.sleep(5)  # Počkáme 5 sekund

        # Vypneme relé (nastavíme pin na LOW)
        GPIO.output(relay_pin, GPIO.LOW)
        print("Relay OFF")
        time.sleep(5)  # Počkáme 5 sekund

except KeyboardInterrupt:
    # Ukončení programu při stisknutí Ctrl+C
    GPIO.cleanup()