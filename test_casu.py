import board
import busio
import adafruit_ds3231



# Definice GPIO pinů pro I2C komunikaci
scl_pin = board.SCL_1  # Pin pro SCL I2C (např. GPIO3)
sda_pin = board.SDA_1  # Pin pro SDA I2C (např. GPIO2)

# Inicializace I2C sběrnice s definovanými piny
i2c = busio.I2C(scl=scl_pin, sda=sda_pin)


# Inicializace objektu RTC
rtc = adafruit_ds3231.DS3231(i2c)

# Čtení aktuálního času z RTC modulu
current_time = rtc.datetime

print("Aktuální čas z RTC:", current_time)
