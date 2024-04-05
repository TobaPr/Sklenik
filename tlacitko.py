import RPi.GPIO as GPIO
import time
import i2clcd

# Nastavení pinů GPIO
button_pin = 16
relay_pin = 19

# Nastavení režimu pinů GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin, GPIO.OUT)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Použití interního pull-up rezistoru

def Vypis_na_LCD(text1, text2):
    # Inicializace LCD displeje
    lcd = i2clcd.i2clcd(i2c_bus=1, i2c_addr=0x27, lcd_width=16)
    lcd.init()
    lcd.set_backlight(True)

    # Výpis textu na displej
    lcd.print_line(text1, line=0)
    lcd.print_line(text2, line=1)


try:
    while True:
        # Přečtení stavu tlačítka
        button_state = GPIO.input(button_pin)
        Vypis_na_LCD('Jsem pripraven', '')

        # Pokud je tlačítko stisknuto (zajímá nás změna stavu z vysokého na nízký)
        if button_state == GPIO.LOW:
            print("Tlačítko stisknuto. Přepínám stav relé.")
            
            Vypis_na_LCD('test', 'Prepinam stav')

            # Přepnutí stavu relé
            relay_state = GPIO.input(relay_pin)
            GPIO.output(relay_pin, not relay_state)

            # Počkejte chvíli, abyste zabránili skoku stavu
            time.sleep(10)
            Vypis_na_LCD('Ahoj', '')

except KeyboardInterrupt:
    print("\nProgram ukončen uživatelem.")
finally:
    # Resetovat GPIO piny na výchozí hodnoty
    GPIO.cleanup()
