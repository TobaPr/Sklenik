import RPi.GPIO as GPIO
import time
import i2clcd
import adafruit_ds3231
import board
import Adafruit_DHT
import Adafruit_ADS1x15


# Nastavení pinů GPIO
button1_pin = 23
button2_pin = 22
button3_pin = 27
button4_pin = 24 


# Nastavení režimu pinů GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(button1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Použití interního pull-up rezistoru
GPIO.setup(button2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Použití interního pull-up rezistoru
GPIO.setup(button3_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Použití interního pull-up 
GPIO.setup(button4_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Použití interního pull-up rezistoru



def Vypis_na_LCD(text):
    # Inicializace LCD displeje
    lcd = i2clcd.i2clcd(i2c_bus=1, i2c_addr=0x27, lcd_width=16)
    lcd.init()
    lcd.set_backlight(True)

    # Výpis textu na displej
    status = Dej_cas() + ' ' + Dej_Teplotu() + ' ' + Dej_vlhkost() + '%'
    #status = status.encode('utf-8')
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

def Dej_Teplotu():
    # Definice typu senzoru a GPIO pinu, na kterém je připojen
    sensor = Adafruit_DHT.DHT22
    pin = 21  # GPIO pin 21 (vyberte si správný pin, na kterém je senzor připojen)

    # Čtení dat ze senzoru
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    # Kontrola, zda byla data úspěšně přečtena
    if temperature is not None:
        # Formátování teploty a vlhkosti do řetězce
        formatted_data = '{0:0.1f}'.format(temperature)
        return formatted_data
    else:
        return 'xx'
    
def Dej_vlhkost():
    adc = Adafruit_ADS1x15.ADS1115()
    value = adc.read_adc(0, gain=1)  # Pokud chcete přesnější hodnoty, můžete změnit gain
    vlhkost = 100 - (value / 32767 * 100)
    return '{:.1f}%'.format(vlhkost)

try:
    Vypis_na_LCD('Jsem pripraven')
    while True:
        # Přečtení stavu tlačítka
        button1_state = GPIO.input(button1_pin)
        button2_state = GPIO.input(button2_pin)
        button3_state = GPIO.input(button3_pin)
        button4_state = GPIO.input(button4_pin)
       

        # Pokud je tlačítko stisknuto (zajímá nás změna stavu z vysokého na nízký)
        if button1_state == GPIO.LOW:
            print("Tlačítko 1 stisknuto.")
            Vypis_na_LCD('Tlacitko 1')

        if button2_state == GPIO.LOW:
            print("Tlačítko 2 stisknuto.")
            Vypis_na_LCD('Tlacitko 2')
        
        if button3_state == GPIO.LOW:
            print("Tlačítko 3 stisknuto.")
            Vypis_na_LCD('Tlacitko 3')

        if button4_state == GPIO.LOW:
            print("Tlačítko 4 stisknuto.")
            Vypis_na_LCD('Tlacitko 4')


except KeyboardInterrupt:
    print("\nProgram ukončen uživatelem.")
finally:
    # Resetovat GPIO piny na výchozí hodnoty
    GPIO.cleanup()
