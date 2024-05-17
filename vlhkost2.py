import board
import busio
import time
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


# Inicializace I2C sběrnice

def calculate_humidity(measurement):
    # Maximální a minimální hodnoty měření
    max_measurement = 30820
    min_measurement = 14550
    max_humidity = 100
    min_humidity = 0
    
    # Výpočet vlhkosti na základě lineární interpolace
    humidity = ((max_measurement - measurement) / (max_measurement - min_measurement)) * 100
    
    # Omezení hodnoty vlhkosti na rozsah 0-100
    humidity = max(min_humidity, min(max_humidity, humidity))
    
    return humidity


try:
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)

    while True:
        channel3 = AnalogIn(ads, ADS.P3)
        channel0 = AnalogIn(ads, ADS.P0)

        #SH = '{:.1f}'.format(100 - (channel3.value / 32767 * 100))
        SH = calculate_humidity(channel3.value)   
        print("chanel 3: Hodnota vlhkosti půdy:", channel3.value)
        print("chanel 3: Hodnota v % :", SH)

        
        #SH2 = '{:.1f}'.format(100 - (channel0.value / 32767 * 100))
        SH2 = calculate_humidity(channel0.value)
            
        print("chanel 0: Hodnota vlhkosti půdy:", channel0.value)
        print("chanel 0: Hodnota v % :", SH2)


        print("-----------------------------")
        time.sleep(5)


except Exception as e: 
    print("Došlo k chybě:", e)
