import board
import busio
import adafruit_ds3231

# Inicializace I2C sběrnice
i2c = busio.I2C(board.GPIO2, board.GPIO3)


# Inicializace objektu RTC
rtc = adafruit_ds3231.DS3231(i2c)

# Čtení aktuálního času z RTC modulu
current_time = rtc.datetime

print("Aktuální čas z RTC:", current_time)
