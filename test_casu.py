import adafruit_ds3231
import time
import board

i2c = board.I2C()  # uses board.SCL and board.SDA


# Inicializace objektu RTC
rtc = adafruit_ds3231.DS3231(i2c)



# Nastavení času RTC na aktuální čas (už není potřeba)
# Získání aktuálního času
# now = time.localtime()
# now2 = time.localtime(time.mktime(now) + 3600)
# rtc.datetime = now2
# print("Čas na RTC modulu byl nastaven na aktuální čas:", now)

# Čtení aktuálního času z RTC modulu
current_time = rtc.datetime


print("Aktuální čas z RTC:")
print("Rok: {:04d}".format(current_time.tm_year))
print("Měsíc: {:02d}".format(current_time.tm_mon))
print("Den: {:02d}".format(current_time.tm_mday))
print("Hodina: {:02d}".format(current_time.tm_hour))
print("Minuta: {:02d}".format(current_time.tm_min))


