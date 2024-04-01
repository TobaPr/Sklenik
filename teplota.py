import Adafruit_DHT

# Definice typu senzoru a GPIO pinu, na kterém je připojen
sensor = Adafruit_DHT.DHT11
pin = 4  # GPIO pin 4 (vyberte si správný pin, na kterém je senzor připojen)

# Čtení dat ze senzoru
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

humidity2, temperature2 = Adafruit_DHT.read(sensor, pin)

# Kontrola, zda byla data úspěšně přečtena
if humidity is not None and temperature is not None:
    print('Teplota: {0:0.1f} °C'.format(temperature))
    print('Vlhkost: {0:0.1f} %'.format(humidity))
    print("Surová hodnota teploty:", temperature2)
    print("Surová hodnota vlhkosti:", humidity2)
else:
    print('Chyba při čtení dat ze senzoru DHT11. Zkontrolujte připojení senzoru a zkuste to znovu.')