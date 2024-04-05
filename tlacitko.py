import RPi.GPIO as GPIO
import time

# Nastavení pinů GPIO
button_pin = 16
relay_pin = 19

# Nastavení režimu pinů GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin, GPIO.OUT)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Použití interního pull-up rezistoru

try:
    while True:
        # Přečtení stavu tlačítka
        button_state = GPIO.input(button_pin)

        # Pokud je tlačítko stisknuto (zajímá nás změna stavu z vysokého na nízký)
        if button_state == GPIO.LOW:
            print("Tlačítko stisknuto. Přepínám stav relé.")

            # Přepnutí stavu relé
            relay_state = GPIO.input(relay_pin)
            GPIO.output(relay_pin, not relay_state)

            # Počkejte chvíli, abyste zabránili skoku stavu
            time.sleep(10)

except KeyboardInterrupt:
    print("\nProgram ukončen uživatelem.")
finally:
    # Resetovat GPIO piny na výchozí hodnoty
    GPIO.cleanup()
