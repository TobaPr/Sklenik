import board
import time
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


try:
    i2c = board.I2C()  
    ads = ADS.ADS1115(i2c)
    # Define the analog input channels
    #channel0 = AnalogIn(ads, ADS.P0)
    #channel1 = AnalogIn(ads, ADS.P1)
    #channel2 = AnalogIn(ads, ADS.P2)

     
    while True:
        channel3 = AnalogIn(ads, ADS.P3)
        SH = '{:.1f}'.format(100 - (channel3.value / 32767 * 100))
            
        print("Hodnota vlhkosti půdy:", channel3.value)
        print("Hodnota v % :", SH)


        time.sleep(5)


except Exception as e: 
    print("Došlo k chybě:", e)
