from w1thermsensor import W1ThermSensor

# Definice čísla GPIO pinu, na kterém je čidlo připojeno
pin = 7  # Například GPIO pin č. 4

# Inicializace senzoru s definovaným pinem
# sensor = W1ThermSensor(GPIO=pin)
sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, pin)

# Čtení teploty
temperature = sensor.get_temperature()

# Výpis teploty
print("Aktuální teplota:", temperature, "°C")