import adafruit_ds3231
import time
import board

i2c = board.I2C()  # uses board.SCL and board.SDA


# Inicializace objektu RTC
rtc = adafruit_ds3231.DS3231(i2c)

# Čtení aktuálního času z RTC modulu
current_time = rtc.datetime

print("Aktuální čas z RTC:")
print("Rok: {:04d}".format(current_time.year))
print("Měsíc: {:02d}".format(current_time.month))
print("Den: {:02d}".format(current_time.day))
print("Hodina: {:02d}".format(current_time.hour))
print("Minuta: {:02d}".format(current_time.minute))
