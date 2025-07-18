import RPi.GPIO as GPIO
import time
import datetime
import schedule
import i2clcd
import adafruit_ds3231
import board
import Adafruit_DHT
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from rak811.rak811_v3 import Rak811



# Konstanty
DoorMovingTime = 60 # doba po kterou se pohybuje motor u dveří
WinMovingTime = 30 # doba po kterou se pohybuje motor u okna
VentilMovingTime = 10 # doba po kterou se pohybuje ventil
FanDelay = 5

# Příznak zda odesíláme data
onlinemode = False


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
GPIO.setup(door_close_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(win_open_pin, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(win_close_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ventil_pin, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(fan_pin, GPIO.OUT, initial=GPIO.HIGH)

def JoinToLora():
    if onlinemode:
        try:
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
            lora.close()
            print("Pripojeno")
        except Exception as e:
            print("Došlo k chybě při připojování k LoRa:", e)

def SendLoraMesagge(text,port):
    if onlinemode:
        try:
            print("Posilam zpravu: " + str(text) + ' '+ str(port))
            lora = Rak811()
            lora.send(text,int(port))
            lora.close()
        except Exception as e:
            print("Došlo k chybě při odesílání zprávy:", e)
    
        
def GetRTCTime():
    # Inicializace objektu RTC
    i2c = board.I2C()  # Pokud již není inicializováno
    rtc = adafruit_ds3231.DS3231(i2c)

    # Čtení aktuálního času z RTC modulu
    current_time = rtc.datetime

    # Formátování času do podoby HH:MM
    formatted_time = "{:02d}:{:02d}".format(current_time.tm_hour, current_time.tm_min)
    return formatted_time
    
def CheckAirStatus():
    try:
        sensor = Adafruit_DHT.DHT22
        pin = 21  # GPIO pin 21 
        # Čtení dat ze senzoru
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        if temperature is not None and humidity is not None:
            AT = '{:.1f}'.format(temperature)
            AH = '{:.1f}'.format(humidity)
        else:
            AT = '{:.1f}'.format(0)
            AH = '{:.1f}'.format(0)
        return AT, AH
    except Exception as e:
        print("Došlo k chybě:", e)
        return 0.0, 0.0


def CalculateSoilHumidity(measurement):
    # Maximální a minimální hodnoty měření
    max_measurement = 14400
    min_measurement = 7820
    max_humidity = 100
    min_humidity = 0
    
    # Výpočet vlhkosti na základě lineární interpolace
    humidity = ((max_measurement - measurement) / (max_measurement - min_measurement)) * 100
    
    # Omezení hodnoty vlhkosti na rozsah 0-100
    humidity = max(min_humidity, min(max_humidity, humidity))
    return humidity


def CheckSoilSatus():
    try:
        i2c = board.I2C()  
        ads = ADS.ADS1115(i2c)
       
        channel0 = AnalogIn(ads, ADS.P0)
        #channel1 = AnalogIn(ads, ADS.P1)
        #channel2 = AnalogIn(ads, ADS.P2)
        channel3 = AnalogIn(ads, ADS.P3)

        SH1 = '{:.1f}'.format(CalculateSoilHumidity(channel0.value))
        SH2 = '{:.1f}'.format(CalculateSoilHumidity(channel3.value))
        return SH1, SH2
    except Exception as e: 
        print("Došlo k chybě:", e)
        return 0.0, 0.0


def PrintStatus(AT, AH, SH1, SH2, RTC):
      # Inicializace LCD displeje
    lcd = i2clcd.i2clcd(i2c_bus=1, i2c_addr=0x27, lcd_width=16)
    lcd.init()
    lcd.set_backlight(True)

    # Sestavení řetězců 
    line1 = RTC + '  ' + str(AT) + ' ' + str(AH) 
    line2 = str(SH1) + ' ' + str(SH2) 

    # Doplnění řetězce na požadovanou délku
    if len(line1) < 16:
        line1 = line1.ljust(16, ' ')

    if len(line2) < 16:
        line2 = line2.rjust(16, ' ')
    lcd.print_line(line1, line=0)
    lcd.print_line(line2, line=1)

    # vytiskneme i v konzoli
    print(line1 + '' + line2)  

def PrintMesagge(line1, line2):
    # Inicializace LCD displeje
    lcd = i2clcd.i2clcd(i2c_bus=1, i2c_addr=0x27, lcd_width=16)
    lcd.init()
    lcd.set_backlight(True)

  # Doplnění řetězce na požadovanou délku
    if len(line1) < 16:
        line1 = line1.ljust(16, ' ')
    if len(line2) < 16:
        line2 = line2.ljust(16, ' ')

    #vytiskneme na LCD 
    lcd.print_line(line1, line=0)
    lcd.print_line(line2, line=1)
    # vytiskneme i v konzoli
    print(line1 + '' + line2)  


def OpenDoor(type):
    # Pro ovevírání a zavírání používáme dvě relé
    if not GPIO.input(door_close_pin):
        GPIO.output(door_close_pin, GPIO.HIGH)
        time.sleep(1) # pro jistotu počkáme (je nutné zabránit tomu aby byli sepnuté obě)
        GPIO.output(door_open_pin, GPIO.LOW)
        PrintMesagge('Oteviram dvere','Odesilam...')
        #Type slouží jako příznak zda jde o manuální otevření nebo automatické
        SendLoraMesagge(type + 'O', 101) 
        PrintMesagge('Oteviram dvere','')
        time.sleep(DoorMovingTime)  # Počkáme než dojede motor... 
        CheckConditions(print=True, send=False)

def CloseDoor(type):
    # pro ovevírání a zavírání používáme dvě relé
    if not GPIO.input(door_open_pin):
        GPIO.output(door_open_pin, GPIO.HIGH)
        time.sleep(1) # pro jistotu počkáme (je nutné zabránit tomu aby byli sepnuté obě)
        GPIO.output(door_close_pin, GPIO.LOW)
        PrintMesagge('Zaviram dvere','Odesilam...')
        SendLoraMesagge(type + 'C', 101) # MC (manual close)
        PrintMesagge('Zaviram dvere','')
        time.sleep(DoorMovingTime)  # Počkáme než dojede motor... 
        CheckConditions(print=True, send=False)

def OpenWindow(type):
    # pro ovevírání a zavírání používáme dvě relé
    if not GPIO.input(win_close_pin):
        GPIO.output(win_close_pin, GPIO.HIGH)
        time.sleep(1) 
        GPIO.output(win_open_pin, GPIO.LOW)
        PrintMesagge('Oteviram okno','Odesilam...')
        SendLoraMesagge(type + 'O', 102) 
        PrintMesagge('Oteviram okno','')
        time.sleep(WinMovingTime)  
        CheckConditions(print=True, send=False)

def CloseWindow(type):
    # pro ovevírání a zavírání používáme dvě relé
    if not GPIO.input(win_open_pin):
        GPIO.output(win_open_pin, GPIO.HIGH)
        time.sleep(1) 
        GPIO.output(win_close_pin, GPIO.LOW)
        PrintMesagge('Zaviram okno','Odesilam...')
        SendLoraMesagge(type +'C', 102) 
        PrintMesagge('Zaviram okno','')
        time.sleep(WinMovingTime)  
        CheckConditions(print=True, send=False)

def OpenValve(type):
    if GPIO.input(ventil_pin):
        GPIO.output(ventil_pin, GPIO.LOW)
        PrintMesagge('Oteviram ventil','Odesilam...')
        SendLoraMesagge(type + 'O', 103) 
        PrintMesagge('Oteviram ventil','')
        time.sleep(VentilMovingTime)
        CheckConditions(print=True, send=False)

def CloseValve(type):
    if not GPIO.input(ventil_pin):
        GPIO.output(ventil_pin, GPIO.HIGH)
        PrintMesagge('Zaviram ventil','Odesilam...')
        SendLoraMesagge(type + 'C', 103)
        PrintMesagge('Zaviram ventil','')
        time.sleep(VentilMovingTime) 
        CheckConditions(print=True, send=False)   

def FanOn(type):
    if GPIO.input(fan_pin):
        GPIO.output(fan_pin, GPIO.LOW)
        PrintMesagge('Zapinam vetrani', 'Odesilam...')
        SendLoraMesagge(type + 'O', 104)
        PrintMesagge('Zapinam vetrani', '')
        time.sleep(FanDelay)
        CheckConditions(print=True, send=False)   

def FanOff(type):
    if not GPIO.input(fan_pin):
        GPIO.output(fan_pin, GPIO.HIGH)
        PrintMesagge('Vypinam vetrani', 'Odesilam...') 
        SendLoraMesagge(str(type) + 'C', 104)
        PrintMesagge('Vypinam vetrani', '') 
        time.sleep(FanDelay)
        CheckConditions(print=True, send=False)   


# Obslužné metody pro tlačítka.
def Button1_Pressed():
    if GPIO.input(door_open_pin): # pokud jsou dveře zavřené 
        OpenDoor('M')
    else:
        CloseDoor('M')
# Obslužná metoda pro tlačítko 2. Ručně Otevírá / zavírá okno.
def Button2_Pressed():
    if GPIO.input(win_open_pin): # pokud je okno zavřené 
        OpenWindow('M')
    else:
        CloseWindow('M')

def Button3_Pressed():
    if GPIO.input(ventil_pin): # pokud je ventil zavreny 
        OpenValve('M')
    else:
        CloseValve('M')

def Button4_Pressed():
    if GPIO.input(fan_pin): 
        FanOn('M')
    else:
        FanOff('M')

def SetDoor(Temperature):
    if Temperature > 32:
        OpenDoor('A')

    if Temperature < 27:
        CloseDoor('A')

def SetWindow(Temperature):
    if Temperature > 28:
        OpenWindow('A')

    if Temperature < 25:
        CloseWindow('A')

def SetValve(SH1, SH2, Hour, Minutes):
    #Ideální čas na zavlažování je večer a ráno (zaléváme jen v 8 večer a 6 ráno)
    if (Hour == 6 or Hour == 20):
        if ((SH1 >= 0 and SH1 < 40) or (SH2 >= 0 and SH2 < 40)):
            OpenValve('A')
        else:
            CloseValve('A')
            #Pravidelná závlaha v období 20:00 až 20:20 .Na jeden cyklus (20 minut) pustíme závlahu bez ohledu na vlhkost půdy.
            if (Hour == 20 and Minutes <= 20):
                OpenValve('S')
            else:
                CloseValve('A')
    else:
        CloseValve('A')

def SetFan(Temperature):
    if Temperature > 37:
        FanOn('A')
    
    if Temperature < 32:
        FanOff('A')


def CheckConditions(print, send, control=False):
    AirTemperature, AirHumidity = CheckAirStatus()
    SoilHumidity1, SoilHumidity2 = CheckSoilSatus()
    RTC = GetRTCTime()
    
    #Reagujeme na podmínky ve skleníku
    if control:    
        hours, minutes = map(int, RTC.split(':'))  
        Temperature = float(AirTemperature)
        SoilHumid1 = float(SoilHumidity1)
        SoilHumid2 = float(SoilHumidity2)
    
        SetValve(SoilHumid1, SoilHumid2, hours, minutes)
        SetDoor(Temperature)
        SetWindow(Temperature)
        SetFan(Temperature)

    #Příznak zda posíláme zprávu
    if send: 
        Conditions = str(AirTemperature) + ';' + str(AirHumidity) + ';' + str(SoilHumidity1) + ';' + str(SoilHumidity2)
        PrintMesagge(RTC, 'Odesilam stav')
        #posíláme podmínky na portu 1
        SendLoraMesagge(Conditions,1) 

    #příznak zda vytiskneme podmínky na LCD display
    if print:
        PrintStatus(AirTemperature, AirHumidity, SoilHumidity1, SoilHumidity2, RTC )       

    

# ---------    Hlavní tělo programu    ---------    
try:
    # Zalogujeme se do LoRa sítě.
    JoinToLora() 

    # Ověříme podmínky ve skleníku, pošleme je a reagujeme na ně.
    CheckConditions(print = True, send= True, control=True) 

    #Každé 3 minuty vytiskneme podmínky na display (bez odesílání a ovládání)
    schedule.every(3).minutes.do(CheckConditions, print=True, send=False, control=False)

    #Každých 20 minut reagujeme na podmínky ve skleníku a posíláme stav přes LoRa a také tiskneme stav na display.
    schedule.every(20).minutes.do(CheckConditions, print=True, send=True, control=True)
    
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
        time.sleep(1) 

except KeyboardInterrupt:
    print("\nProgram ukončen uživatelem.")
finally:
    # Resetovat GPIO piny na výchozí hodnoty
    GPIO.cleanup()
