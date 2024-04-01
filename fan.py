import RPi.GPIO as GPIO
import time

# Nastavení režimu pinu na GPIO.BOARD
GPIO.setmode(GPIO.BOARD)

# Nastavení pinu GPIO jako výstupního
pwm_pin = 12  # Přizpůsobte číslo pinu podle vašeho zapojení
GPIO.setup(pwm_pin, GPIO.OUT)

# Inicializace PWM na pinu s frekvencí 100 Hz
pwm = GPIO.PWM(pwm_pin, 100)

pwm.start(100) 
print('100%')
time.sleep(10)  # Počkáme 10 sekund
pwm.ChangeDutyCycle(10)
print('10%')
time.sleep(10)  # Počkáme 10 sekund
pwm.ChangeDutyCycle(100)
print('100%')
time.sleep(10)  # Počkáme 10 sekund
pwm.ChangeDutyCycle(20)
print('20%')
time.sleep(10)  # Počkáme 10 sekund
pwm.ChangeDutyCycle(1)
print('1%')
time.sleep(10)  # Počkáme 10 sekund


pwm.stop()
GPIO.cleanup()
