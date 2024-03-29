import adafruit_ds3231
import time
import board

i2c = board.I2C()  # uses board.SCL and board.SDA


# Inicializace objektu RTC
rtc = adafruit_ds3231.DS3231(i2c)

# Čtení aktuálního času z RTC modulu
current_time = rtc.datetime

current_time2 = time.localtime()

print("Aktuální čas z RTC:")
print("Rok: {:04d}".format(current_time.tm_year))
print("Měsíc: {:02d}".format(current_time.tm_mon))
print("Den: {:02d}".format(current_time.tm_mday))
print("Hodina: {:02d}".format(current_time.tm_hour))
print("Minuta: {:02d}".format(current_time.tm_min))


print("Aktuální čas z time...:")
print("Rok: {:04d}".format(current_time2.tm_year))
print("Měsíc: {:02d}".format(current_time2.tm_mon))
print("Den: {:02d}".format(current_time2.tm_mday))
print("Hodina: {:02d}".format(current_time2.tm_hour))
print("Minuta: {:02d}".format(current_time2.tm_min))