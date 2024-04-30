import RPi.GPIO as GPIO
import time
import datetime
import schedule
import i2clcd
import adafruit_ds3231
import board
import Adafruit_DHT
import Adafruit_ADS1x15
from rak811.rak811_v3 import Rak811


# Konstanty
DoorMovingTime = 3 # doba po kterou se pohybuje motor u dveří
WinMovingTime = 3 # doba po kterou se pohybuje motor u okna
VentilMovingTime = 3 # doba po kterou se pohybuje ventil
FanDelay = 3

#Globalni proměnne... 
AirTemperature = 0
AirHumidity =  0
SoilHumidity1 = 0
SoilHumidity2 = 0


# Nastavení pinů pro ovládání tlačítek
button1_pin = 23
button2_pin = 22
button3_pin = 27
button4_pin = 24 

# Definujeme pin pro ovládání relé
door_open_pin = 5
door_close_pin = 6
win_open_pin = 13
win_close_pin = 19
ventil_pin = 16
fan_pin = 20

# Nastavení režimu pinů GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(button1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Použití interního pull-up rezistoru
GPIO.setup(button2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(button3_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(button4_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(door_open_pin, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(door_close_pin, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(win_open_pin, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(win_close_pin, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(ventil_pin, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(fan_pin, GPIO.OUT, initial=GPIO.HIGH)




def JoinToLora():
    lora = Rak811()
    lora.set_config('lora:work_mode:0')
    lora.set_config('lora:join_mode:0')
    lora.set_config('lora:region:EU868')
    lora.set_config('lora:app_eui:AC1F09FFF8680811')
    lora.set_config('lora:app_key:AC1F09FFFE03DD04AC1F09FFF8680811')
    lora.join()
    lora.set_config('lora:dr:5')
    print("připojuji se")
    lora.send('Start',100)
    print("poslal jsem zprávu")
    lora.close()
    print("joinul jsem se a zaviram")

def SendMesagge(text,port):
    print("posilam zpravu")
    lora = Rak811()
    lora.send(text,101)
    lora.close()


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


def GetActualDateTime():
    # Inicializace objektu RTC
    i2c = board.I2C()  # Pokud již není inicializováno
    rtc = adafruit_ds3231.DS3231(i2c)

    # Čtení aktuálního času z RTC modulu
    current_time = rtc.datetime
    return current_time
    

def Dej_Teplotu():
    # Definice typu senzoru a GPIO pinu, na kterém je připojen
    sensor = Adafruit_DHT.DHT22
    pin = 21  # GPIO pin 21 (vyberte si správný pin, na kterém je senzor připojen)

    # Čtení dat ze senzoru
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    # Kontrola, zda byla data úspěšně přečtena
    if temperature and humidity is not None:
        # Formátování teploty a vlhkosti do řetězce
        formatted_data = '{0:0.1f}'.format(temperature)
        return formatted_data
    else:
        return 'xx'
    
def CheckAirStatus():
    sensor = Adafruit_DHT.DHT22
    pin = 21  # GPIO pin 21 
    # Čtení dat ze senzoru
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if temperature and humidity is not None:
        AirTemperature = '{:.1f}'.format(temperature)
        AirHumidity = '{:.1f}'.format(humidity)
    else:
        AirTemperature = '{:.1f}'.format(0)
        AirHumidity = '{:.1f}'.format(0)


    
def Dej_vlhkost():
    adc = Adafruit_ADS1x15.ADS1115()
    value = adc.read_adc(0, gain=1)  # Pokud chcete přesnější hodnoty, můžete změnit gain
    vlhkost = 100 - (value / 32767 * 100)
    return '{:.1f}%'.format(vlhkost)

def CheckSoilSatus():
    adc = Adafruit_ADS1x15.ADS1115()
    Sensor1 = adc.read_adc(0, gain=1)  # Pokud chcete přesnější hodnoty, můžete změnit gain
    Sensor2 = adc.read_adc(3, gain=1) 
    SoilHumidity1 = '{:.1f}'.format(100 - (Sensor1 / 32767 * 100))
    SoilHumidity2 = '{:.1f}'.format(100 - (Sensor2 / 32767 * 100))
    
def PrintStatus():
      # Inicializace LCD displeje
    lcd = i2clcd.i2clcd(i2c_bus=1, i2c_addr=0x27, lcd_width=16)
    lcd.init()
    lcd.set_backlight(True)

    # Sestavení řetězců 
    line1 = Dej_cas() + ' ' + AirTemperature + ' ' + AirHumidity
    
    # Doplnění řetězce na požadovanou délku
    if len(line1) < 16:
        line1 = line1.ljust(16, ' ')
    line2 = SoilHumidity1 + SoilHumidity2
    if len(line2) < 16:
        line2 = line2.rjust(16, ' ')

    lcd.print_line(line1, line=0)
    lcd.print_line(line2, line=1)

def PrintMesagge(line1, line2):
    # Inicializace LCD displeje
    lcd = i2clcd.i2clcd(i2c_bus=1, i2c_addr=0x27, lcd_width=16)
    lcd.init()
    lcd.set_backlight(True)
  # Doplnění řetězce na požadovanou délku
    if len(line1) < 16:
        line1 = line1.ljust(16, ' ')
    line2 = SoilHumidity1 + SoilHumidity2
    if len(line2) < 16:
        line2 = line2.ljust(16, ' ')
    lcd.print_line(line1, line=0)
    lcd.print_line(line2, line=1)


def Otevri_dvere():
    # pro ovevírání a zavírání používáme dvě relé
    GPIO.output(door_close_pin, GPIO.HIGH)
    time.sleep(1) # pro jistotu počkáme (je nutné zabránit tomu aby byli sepnuté obě)
    GPIO.output(door_open_pin, GPIO.LOW)
    print("Otevírám dveře")
    SendMesagge('O', 101)
    PrintMesagge('Oteviram dvere..','')
    time.sleep(DoorMovingTime)  # Počkáme než dojede motor... 
    PrintStatus()

def Zavri_dvere():
    # pro ovevírání a zavírání používáme dvě relé
    GPIO.output(door_open_pin, GPIO.HIGH)
    time.sleep(1) # pro jistotu počkáme (je nutné zabránit tomu aby byli sepnuté obě)
    GPIO.output(door_close_pin, GPIO.LOW)
    print("Zavirám dveře")
    SendMesagge('C', 101)
    PrintMesagge('Zaviram dvere...','')
    time.sleep(DoorMovingTime)  # Počkáme než dojede motor... 
    PrintStatus()

def Otevri_okno():
    # pro ovevírání a zavírání používáme dvě relé
    GPIO.output(win_close_pin, GPIO.HIGH)
    time.sleep(1) # pro jistotu počkáme (je nutné zabránit tomu aby byli sepnuté obě)
    GPIO.output(win_open_pin, GPIO.LOW)
    print("Otevírám okno")
    Vypis_na_LCD('Oteviram okno...')
    time.sleep(WinMovingTime)  # Počkáme než dojede motor... 

def Zavri_okno():
    # pro ovevírání a zavírání používáme dvě relé
    GPIO.output(win_open_pin, GPIO.HIGH)
    time.sleep(1) # pro jistotu počkáme (je nutné zabránit tomu aby byli sepnuté obě)
    GPIO.output(win_close_pin, GPIO.LOW)
    print("Zavirám okno")
    Vypis_na_LCD('Zaviram okno....')
    time.sleep(WinMovingTime)  # Počkáme než dojede motor... 

def Otevri_ventil():
    GPIO.output(ventil_pin, GPIO.LOW)
    print("Otevírám ventil")
    Vypis_na_LCD('Oteviram ventil.')
    time.sleep(VentilMovingTime)

def Zavri_ventil():
    GPIO.output(ventil_pin, GPIO.HIGH)
    print("Zavírám ventil")
    Vypis_na_LCD('Zaviram ventil..')
    time.sleep(VentilMovingTime)    

def FAN_ON():
    GPIO.output(fan_pin, GPIO.LOW)
    print("Zapinam vetrani")
    Vypis_na_LCD('Zapinam vetrani.')
    time.sleep(FanDelay)

def FAN_OFF():
    GPIO.output(fan_pin, GPIO.HIGH)
    print("Vypinam vetrani")
    Vypis_na_LCD('Vypinam vetrani.') 

# Obslužné metody pro tlačítka.
def Button1_Pressed():
    if GPIO.input(door_open_pin): # pokud jsou dveře zavřené 
        Otevri_dvere()
    else:
        Zavri_dvere()

def Button2_Pressed():
    # Obslužná metoda pro tlačítko 2. Ručně Otevírá / zavírá okno.
    if GPIO.input(win_open_pin): # pokud je okno zavřené 
        Otevri_okno()
    else:
        Zavri_okno()

def Button3_Pressed():
    if GPIO.input(ventil_pin): # pokud je ventil zavreny 
        Otevri_ventil()
    else:
        Zavri_ventil()

def Button4_Pressed():
    if GPIO.input(fan_pin): # pokud je ventil zavreny 
        FAN_ON()
    else:
        FAN_OFF()

def CheckConditions():
    
    CheckAirStatus()
    CheckSoilSatus()

    PrintStatus()





# ---------    Hlavní tělo programu    ---------    
try:
    JoinToLora() # Zalogujeme se do sítě
    CheckConditions() # Ověříme podmínky ve skleníku
    
    schedule.evry(1).minutes.do(CheckConditions)
    

    while True:
    
        # Přečtení stavu tlačítka
        button1_state = GPIO.input(button1_pin)
        button2_state = GPIO.input(button2_pin)
        button3_state = GPIO.input(button3_pin)
        button4_state = GPIO.input(button4_pin)

        # Pokud je tlačítko stisknuto (zajímá nás změna stavu z vysokého na nízký)
        if button1_state == GPIO.LOW:
            Button1_Pressed() # dveře

        if button2_state == GPIO.LOW:
            Button2_Pressed() # okno
           
        if button3_state == GPIO.LOW:
            Button3_Pressed() # ventil

        if button4_state == GPIO.LOW:
            Button4_Pressed() # vetrak

        schedule.run_pending()
        time.sleep(1) ##


except KeyboardInterrupt:
    print("\nProgram ukončen uživatelem.")
finally:
    # Resetovat GPIO piny na výchozí hodnoty
    GPIO.cleanup()
