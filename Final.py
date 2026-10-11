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
DoorMovingTime = 90 # doba po kterou se pohybuje motor u dveří
WinMovingTime = 60 # doba po kterou se pohybuje motor u okna
VentilMovingTime = 10 # doba po kterou se pohybuje ventil
FanDelay = 5

# Příznak zda odesíláme data
onlinemode = False

# Rezim automatickeho ovladani okna:
# 'sun' = 20 min po vychodu a zapadu slunce (Blatnicka, offline)
# 'time' = puvodni casy 06:00-20:00
# 'temperature' = puvodni teplotni ovladani
window_control_mode = 'sun'
SUN_OFFSET_MINUTES = 20

# RTC neprizpusobuje letni a zimni cas. Musi bezet ve STALEM pasmovem case.
# 1 = CET / UTC+1 (trvaly zimni cas), 2 = CEST / UTC+2 (trvaly letni cas).
# RTC je nastaven na trvaly letni cas (UTC+2), bez sezonniho prepinani.
# Casova tabulka je v CET; pro jine nastaveni RTC se casy jen posunou.
RTC_FIXED_UTC_OFFSET_HOURS = 2


# Predpocitane vychody a zapady slunce pro Blatnicku (48.9358431 N, 17.5315778 E).
# Casove hodnoty jsou minuty od pulnoci ve STALEM pasmovem case CET (UTC+1).
# Zakladni kalendar je prestupny rok 2024 (vcetne 29. 2.); pro dalsi roky je
# odchylka astronomickych casu zpravidla radove jednotky minut.
# Zdroj vypoctu: astronomicke rovnice NOAA (zenit 90,833 stupne).
# Indexovani: SUN_TIMES[mesic - 1][den - 1] -> (vychod, zapad).
SUN_TIMES = (
    (  # leden
        (464, 963), (464, 964), (464, 965), (463, 966),
        (463, 967), (463, 968), (463, 969), (462, 971),
        (462, 972), (462, 973), (461, 974), (461, 976),
        (460, 977), (459, 978), (459, 980), (458, 981),
        (457, 983), (456, 984), (456, 986), (455, 987),
        (454, 989), (453, 990), (452, 992), (451, 993),
        (450, 995), (449, 997), (447, 998), (446, 1000),
        (445, 1001), (444, 1003), (442, 1005),
    ),
    (  # unor
        (441, 1006), (440, 1008), (438, 1010), (437, 1011),
        (435, 1013), (434, 1015), (432, 1016), (431, 1018),
        (429, 1020), (428, 1021), (426, 1023), (424, 1024),
        (423, 1026), (421, 1028), (419, 1029), (418, 1031),
        (416, 1033), (414, 1034), (412, 1036), (410, 1038),
        (409, 1039), (407, 1041), (405, 1043), (403, 1044),
        (401, 1046), (399, 1047), (397, 1049), (395, 1051),
        (393, 1052),
    ),
    (  # brezen
        (391, 1054), (389, 1055), (387, 1057), (385, 1059),
        (383, 1060), (381, 1062), (379, 1063), (377, 1065),
        (375, 1066), (373, 1068), (371, 1069), (369, 1071),
        (367, 1073), (365, 1074), (363, 1076), (360, 1077),
        (358, 1079), (356, 1080), (354, 1082), (352, 1083),
        (350, 1085), (348, 1086), (346, 1088), (344, 1089),
        (341, 1091), (339, 1092), (337, 1094), (335, 1095),
        (333, 1097), (331, 1098), (329, 1100),
    ),
    (  # duben
        (327, 1101), (325, 1103), (323, 1104), (321, 1106),
        (318, 1107), (316, 1109), (314, 1110), (312, 1112),
        (310, 1113), (308, 1115), (306, 1116), (304, 1118),
        (302, 1119), (300, 1121), (298, 1122), (296, 1124),
        (294, 1125), (292, 1127), (290, 1128), (289, 1130),
        (287, 1131), (285, 1133), (283, 1134), (281, 1136),
        (279, 1137), (277, 1139), (276, 1140), (274, 1142),
        (272, 1143), (270, 1145),
    ),
    (  # kveten
        (269, 1146), (267, 1148), (265, 1149), (264, 1150),
        (262, 1152), (260, 1153), (259, 1155), (257, 1156),
        (256, 1158), (254, 1159), (253, 1160), (252, 1162),
        (250, 1163), (249, 1165), (247, 1166), (246, 1167),
        (245, 1169), (244, 1170), (242, 1171), (241, 1172),
        (240, 1174), (239, 1175), (238, 1176), (237, 1177),
        (236, 1178), (235, 1180), (234, 1181), (233, 1182),
        (233, 1183), (232, 1184), (231, 1185),
    ),
    (  # cerven
        (230, 1186), (230, 1187), (229, 1188), (229, 1189),
        (228, 1189), (228, 1190), (227, 1191), (227, 1192),
        (226, 1192), (226, 1193), (226, 1194), (226, 1194),
        (226, 1195), (225, 1195), (225, 1196), (225, 1196),
        (225, 1197), (225, 1197), (226, 1197), (226, 1197),
        (226, 1198), (226, 1198), (226, 1198), (227, 1198),
        (227, 1198), (228, 1198), (228, 1198), (229, 1198),
        (229, 1198), (230, 1197),
    ),
    (  # cervenec
        (230, 1197), (231, 1197), (232, 1196), (232, 1196),
        (233, 1196), (234, 1195), (235, 1195), (236, 1194),
        (237, 1193), (237, 1193), (238, 1192), (239, 1191),
        (240, 1190), (241, 1190), (242, 1189), (244, 1188),
        (245, 1187), (246, 1186), (247, 1185), (248, 1184),
        (249, 1183), (251, 1181), (252, 1180), (253, 1179),
        (254, 1178), (256, 1177), (257, 1175), (258, 1174),
        (259, 1172), (261, 1171), (262, 1170),
    ),
    (  # srpen
        (263, 1168), (265, 1167), (266, 1165), (267, 1164),
        (269, 1162), (270, 1160), (272, 1159), (273, 1157),
        (274, 1155), (276, 1154), (277, 1152), (279, 1150),
        (280, 1148), (281, 1147), (283, 1145), (284, 1143),
        (286, 1141), (287, 1139), (288, 1137), (290, 1135),
        (291, 1134), (293, 1132), (294, 1130), (296, 1128),
        (297, 1126), (298, 1124), (300, 1122), (301, 1120),
        (303, 1118), (304, 1116), (306, 1114),
    ),
    (  # zari
        (307, 1112), (308, 1109), (310, 1107), (311, 1105),
        (313, 1103), (314, 1101), (316, 1099), (317, 1097),
        (318, 1095), (320, 1093), (321, 1091), (323, 1088),
        (324, 1086), (325, 1084), (327, 1082), (328, 1080),
        (330, 1078), (331, 1076), (333, 1074), (334, 1071),
        (335, 1069), (337, 1067), (338, 1065), (340, 1063),
        (341, 1061), (343, 1059), (344, 1056), (346, 1054),
        (347, 1052), (348, 1050),
    ),
    (  # rijen
        (350, 1048), (351, 1046), (353, 1044), (354, 1042),
        (356, 1040), (357, 1038), (359, 1036), (360, 1033),
        (362, 1031), (363, 1029), (365, 1027), (366, 1025),
        (368, 1023), (369, 1021), (371, 1019), (372, 1017),
        (374, 1016), (375, 1014), (377, 1012), (379, 1010),
        (380, 1008), (382, 1006), (383, 1004), (385, 1002),
        (386, 1001), (388, 999), (390, 997), (391, 995),
        (393, 994), (394, 992), (396, 990),
    ),
    (  # listopad
        (397, 989), (399, 987), (401, 985), (402, 984),
        (404, 982), (405, 981), (407, 979), (409, 978),
        (410, 977), (412, 975), (413, 974), (415, 973),
        (417, 971), (418, 970), (420, 969), (421, 968),
        (423, 967), (424, 965), (426, 964), (427, 963),
        (429, 962), (430, 961), (432, 961), (433, 960),
        (435, 959), (436, 958), (437, 957), (439, 957),
        (440, 956), (441, 956),
    ),
    (  # prosinec
        (443, 955), (444, 955), (445, 954), (446, 954),
        (448, 954), (449, 953), (450, 953), (451, 953),
        (452, 953), (453, 953), (454, 953), (455, 953),
        (456, 953), (456, 953), (457, 953), (458, 953),
        (459, 954), (459, 954), (460, 954), (461, 955),
        (461, 955), (462, 956), (462, 956), (462, 957),
        (463, 958), (463, 958), (463, 959), (463, 960),
        (464, 961), (464, 962), (464, 963),
    ),
)


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

# Stavy potřebné pro ovledání tlačítek
Door_state = False
# Po startu nezname skutecnou polohu okna, dokud neprikazeme prvni pohyb.
# Je nutne mit funkcni koncove spinace, protoze pri startu muze byt jiz v cili.
Win_state = None
# Posledni solarni faze (den/noc). Zmena spousti prislusny povel jen jednou.
# Rucni prepnuti tak zustane zachovano do nejblizsiho solarniho prechodu.
_sun_last_phase = None
Valve_state = False
Fan_state = False


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
    
        
_rtc_instance = None


def GetRTCDateTime():
    """Vrati datum a cas z RTC DS3231 (bez zavislosti na internetu)."""
    global _rtc_instance
    if _rtc_instance is None:
        _rtc_instance = adafruit_ds3231.DS3231(board.I2C())
    return _rtc_instance.datetime


def GetRTCTime():
    current_time = GetRTCDateTime()
    return "{:02d}:{:02d}".format(current_time.tm_hour, current_time.tm_min)


def GetSunWindowTimes(current_time):
    """Vypoctene spoustece v minutach od pulnoci, v pevnem case RTC.

    Tabulka ma 366 zaznamu v CET (bez DST), opakuje se kazdy rok.
    Pro astronomickou odchylku mezi roky muze jit o radove jednotky minut.
    """
    sunrise, sunset = SUN_TIMES[current_time.tm_mon - 1][current_time.tm_mday - 1]
    rtc_shift = (RTC_FIXED_UTC_OFFSET_HOURS - 1) * 60
    return (sunrise + SUN_OFFSET_MINUTES + rtc_shift,
            sunset + SUN_OFFSET_MINUTES + rtc_shift)


def SetWindowBySun(current_time=None):
    """Otevre 20 minut po vychodu a zavre 20 minut po zapadu slunce."""
    global _sun_last_phase
    if current_time is None:
        current_time = GetRTCDateTime()

    # Pri vybite RTC baterii / chybnem datu nepohybujeme motorem.
    if not (2024 <= current_time.tm_year <= 2099):
        print('Neplatny rok RTC, solarni ovladani okna preskoceno.')
        return
    # Overime take den a mesic (napr. 30. unora) pred pristupem do tabulky.
    try:
        datetime.date(current_time.tm_year, current_time.tm_mon, current_time.tm_mday)
    except ValueError:
        print('Neplatne datum RTC, solarni ovladani okna preskoceno.')
        return

    open_time, close_time = GetSunWindowTimes(current_time)
    now = current_time.tm_hour * 60 + current_time.tm_min
    should_open = open_time <= now < close_time

    # Prvni spusteni zarovna okno do spravne polohy; dale reagujeme jen na
    # prechod noc->den / den->noc. Kontrola probiha v ramci 20min cyklu.
    if _sun_last_phase is should_open:
        return

    print('Solarni ovladani okna {}: otevreni {:02d}:{:02d}, zavreni {:02d}:{:02d}, RTC {:02d}:{:02d}'.format(
        '{}-{:02d}-{:02d}'.format(current_time.tm_year, current_time.tm_mon, current_time.tm_mday),
        open_time // 60, open_time % 60, close_time // 60, close_time % 60,
        current_time.tm_hour, current_time.tm_min))

    # Polohu zname pouze z posledniho povelu, nikoliv ze snimace.
    if should_open and Win_state is not True:
        OpenWindow('A')
    elif not should_open and Win_state is not False:
        CloseWindow('A')
    # Aktualizace az po uspesnem pohybu; pri chybe lze zkusit povel znovu.
    _sun_last_phase = should_open


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
    global Door_state
    # Pro ovevírání a zavírání používáme dvě relé
    GPIO.output(door_close_pin, GPIO.HIGH)
    time.sleep(1) # pro jistotu počkáme (je nutné zabránit tomu aby byli sepnuté obě)
    GPIO.output(door_open_pin, GPIO.LOW)
    PrintMesagge('Oteviram dvere','Odesilam...')
    #Type slouží jako příznak zda jde o manuální otevření nebo automatické
    SendLoraMesagge(type + 'O', 101) 
    PrintMesagge('Oteviram dvere','')
    time.sleep(DoorMovingTime)  # Počkáme než dojede motor... 
    GPIO.output(door_open_pin, GPIO.HIGH)
    Door_state = True
    CheckConditions(print=True, send=False)

def CloseDoor(type):
    global Door_state
    # pro ovevírání a zavírání používáme dvě relé
    GPIO.output(door_open_pin, GPIO.HIGH)
    time.sleep(1) # pro jistotu počkáme (je nutné zabránit tomu aby byli sepnuté obě)
    GPIO.output(door_close_pin, GPIO.LOW)
    PrintMesagge('Zaviram dvere','Odesilam...')
    SendLoraMesagge(type + 'C', 101) # MC (manual close)
    PrintMesagge('Zaviram dvere','')
    time.sleep(DoorMovingTime)  # Počkáme než dojede motor... 
    GPIO.output(door_close_pin, GPIO.HIGH)
    Door_state = False
    CheckConditions(print=True, send=False)

def OpenWindow(type):
    global Win_state
    # Nejsou dovoleny oba smery soucasne.
    GPIO.output(win_close_pin, GPIO.HIGH)
    time.sleep(1)
    try:
        GPIO.output(win_open_pin, GPIO.LOW)
        PrintMesagge('Oteviram okno','Odesilam...')
        SendLoraMesagge(type + 'O', 102)
        PrintMesagge('Oteviram okno','')
        time.sleep(WinMovingTime)
    finally:
        # Pri chybe periferie nebo preruseni vypneme rele motoru.
        GPIO.output(win_open_pin, GPIO.HIGH)
    Win_state = True
    CheckConditions(print=True, send=False)

def CloseWindow(type):
    global Win_state
    GPIO.output(win_open_pin, GPIO.HIGH)
    time.sleep(1)
    try:
        GPIO.output(win_close_pin, GPIO.LOW)
        PrintMesagge('Zaviram okno','Odesilam...')
        SendLoraMesagge(type + 'C', 102)
        PrintMesagge('Zaviram okno','')
        time.sleep(WinMovingTime)
    finally:
        GPIO.output(win_close_pin, GPIO.HIGH)
    Win_state = False
    CheckConditions(print=True, send=False)

def OpenValve(type):
    global Valve_state
    GPIO.output(ventil_pin, GPIO.LOW)
    PrintMesagge('Oteviram ventil','Odesilam...')
    SendLoraMesagge(type + 'O', 103) 
    PrintMesagge('Oteviram ventil','')
    time.sleep(VentilMovingTime)
    Valve_state = True
    CheckConditions(print=True, send=False)

def CloseValve(type):
    global Valve_state
    GPIO.output(ventil_pin, GPIO.HIGH)
    PrintMesagge('Zaviram ventil','Odesilam...')
    SendLoraMesagge(type + 'C', 103)
    PrintMesagge('Zaviram ventil','')
    time.sleep(VentilMovingTime) 
    Valve_state = False
    CheckConditions(print=True, send=False)   

def FanOn(type):
    global Fan_state
    GPIO.output(fan_pin, GPIO.LOW)
    PrintMesagge('Zapinam vetrani', 'Odesilam...')
    SendLoraMesagge(type + 'O', 104)
    PrintMesagge('Zapinam vetrani', '')
    time.sleep(FanDelay)
    Fan_state = True
    CheckConditions(print=True, send=False)   

def FanOff(type):
    global Fan_state
    GPIO.output(fan_pin, GPIO.HIGH)
    PrintMesagge('Vypinam vetrani', 'Odesilam...') 
    SendLoraMesagge(str(type) + 'C', 104)
    PrintMesagge('Vypinam vetrani', '') 
    time.sleep(FanDelay)
    Fan_state = False
    CheckConditions(print=True, send=False)   


# Obslužné metody pro tlačítka.
def Button1_Pressed():
    if Door_state == False: # pokud jsou dveře zavřené 
        OpenDoor('M')
    else:
        CloseDoor('M')
# Obslužná metoda pro tlačítko 2. Ručně Otevírá / zavírá okno.
def Button2_Pressed():
    if Win_state == False: # pokud je okno zavřené
        OpenWindow('M')
    else:
        CloseWindow('M')

def Button3_Pressed():
    if Valve_state == False: # pokud je ventil zavreny 
        OpenValve('M')
    else:
        CloseValve('M')

def Button4_Pressed():
    if Fan_state == False:
        FanOn('M')
    else:
        FanOff('M')

def SetDoor(Temperature):
    if Temperature > 32:
        OpenDoor('A')

    if Temperature < 27:
        CloseDoor('A')

def SetWindow(Temperature, Hour):
    # Zachovame i puvodni rezimy, ale bez opakovanych zbytecnych sepnutí.
    if window_control_mode == 'sun':
        SetWindowBySun()
    elif window_control_mode == 'temperature':
        if Temperature > 28 and Win_state == False:
            OpenWindow('A')
        elif Temperature < 25 and Win_state is not False:
            CloseWindow('A')
    elif window_control_mode == 'time':
        should_open = 6 <= Hour < 20
        if should_open and Win_state is not True:
            OpenWindow('A')
        elif not should_open and Win_state is not False:
            CloseWindow('A')
    else:
        print('Neznamy rezim rizeni okna:', window_control_mode)

def SetValve(SH1, SH2, Hour, Minutes):
    #Ideální čas na zavlažování je večer a ráno (zaléváme jen v 8 večer a 6 ráno)
    if (Hour == 6 or Hour == 20):
        if ((SH1 >= 0 and SH1 < 40) or (SH2 >= 0 and SH2 < 40)):
            OpenValve('A')
        else:
            CloseValve('A')
            #Pravidelná závlaha
            if (Hour == 20 and Minutes <= 20):
                OpenValve('S')
            else:
                CloseValve('A')
    else:
        CloseValve('A')

def SetFan(Temperature):
    if Temperature > 37:
        FanOn('A')
    
    if Temperature < 35:
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
        SetWindow(Temperature, hours)
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
