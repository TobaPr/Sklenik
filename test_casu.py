import board
import busio
import adafruit_ds3231



# Definice GPIO pinů pro I2C komunikaci
sda_pin = board.GPIO27  # GPIO27 pro SDA
scl_pin = board.GPIO22  # GPIO22 pro SCL

# Inicializace I2C sběrnice s definovanými piny
i2c = busio.I2C(scl=scl_pin, sda=sda_pin)


# Inicializace objektu RTC
rtc = adafruit_ds3231.DS3231(i2c)

# Čtení aktuálního času z RTC modulu
current_time = rtc.datetime

print("Aktuální čas z RTC:", current_time)
