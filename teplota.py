from w1thermsensor import W1ThermSensor

# Definice čísla GPIO pinu, na kterém je čidlo připojeno
pin = 21  # Například GPIO pin č. 4

# Inicializace senzoru s definovaným pinem
sensor = W1ThermSensor(GPIO=pin)

# Čtení teploty
temperature = sensor.get_temperature()

# Výpis teploty
print("Aktuální teplota:", temperature, "°C")