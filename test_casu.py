import board
import busio
import adafruit_ds3231





# Inicializace I2C sběrnice s definovanými piny
i2c = busio.I2C(scl=15, sda=13)


# Inicializace objektu RTC
rtc = adafruit_ds3231.DS3231(i2c)

# Čtení aktuálního času z RTC modulu
current_time = rtc.datetime

print("Aktuální čas z RTC:", current_time)
