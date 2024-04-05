import RPi.GPIO as GPIO
import time
import i2clcd
import adafruit_ds3231
import board

# Nastavení pinů GPIO
button_pin = 16
relay_pin = 19

# Nastavení režimu pinů GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin, GPIO.OUT)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Použití interního pull-up rezistoru


def Vypis_na_LCD(text):
    # Inicializace LCD displeje
    lcd = i2clcd.i2clcd(i2c_bus=1, i2c_addr=0x27, lcd_width=16)
    lcd.init()
    lcd.set_backlight(True)

    # Výpis textu na displej
    status = Dej_cas()

    lcd.print_line(status, line=0)
    lcd.print_line(text, line=1)

def Dej_cas():
    # Inicializace objektu RTC
    i2c = board.I2C()  # Pokud již není inicializováno
    rtc = adafruit_ds3231.DS3231(i2c)

    # Čtení aktuálního času z RTC modulu
    current_time = rtc.datetime

    # Formátování času do podoby HH:MM
    formatted_time = "{:02d}:{:02d}".format(current_time.tm_hour, current_time.tm_min)
    
    return formatted_time

try:
    Vypis_na_LCD('Jsem pripraven')
    while True:
        # Přečtení stavu tlačítka
        button_state = GPIO.input(button_pin)
       

        # Pokud je tlačítko stisknuto (zajímá nás změna stavu z vysokého na nízký)
        if button_state == GPIO.LOW:
            print("Tlačítko stisknuto. Přepínám stav relé.")
            
            Vypis_na_LCD('Prepinam stav')

            # Přepnutí stavu relé
            relay_state = GPIO.input(relay_pin)
            GPIO.output(relay_pin, not relay_state)

            # Počkejte chvíli, abyste zabránili skoku stavu
            time.sleep(10)
            Vypis_na_LCD('')

except KeyboardInterrupt:
    print("\nProgram ukončen uživatelem.")
finally:
    # Resetovat GPIO piny na výchozí hodnoty
    GPIO.cleanup()
