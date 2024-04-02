import time
import Adafruit_ADS1x15

# Inicializace ADS1115
adc = Adafruit_ADS1x15.ADS1115()

# Nastavení zesílení (volitelné)
# ADS1115.PGA_4_096V = +/-4.096V
# ADS1115.PGA_2_048V = +/-2.048V
# ADS1115.PGA_1_024V = +/-1.024V
# ADS1115.PGA_0_512V = +/-0.512V
# ADS1115.PGA_0_256V = +/-0.256V
GAIN = 1

# Kanál, na kterém je připojen senzor vlhkosti půdy
# Ujistěte se, že je správně vybrán kanál podle zapojení
channel = 0

# Funkce pro čtení hodnoty vlhkosti půdy
def read_soil_moisture():
    # Přečtení hodnoty z ADS1115
    value = adc.read_adc(channel, gain=GAIN)
    # Interpretace hodnoty vlhkosti půdy - záleží na konkrétním senzoru
    # Můžete použít datasheet senzoru nebo provést kalibraci
    # Tento kód pouze zobrazuje načtenou hodnotu
    return value

try:
    while True:
        # Čtení a výpis hodnoty vlhkosti půdy každou sekundu
        soil_moisture = read_soil_moisture()
        print("Hodnota vlhkosti půdy:", soil_moisture)
        time.sleep(5)
except KeyboardInterrupt:
    # Po ukončení programu provede čištění GPIO a vypne LED
    GPIO.cleanup()
