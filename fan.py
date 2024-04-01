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

try:
    time.sleep(10)  # Počkáme 10 sekund

    # Snížíme duty cycle o 30 %
    new_duty_cycle = max(0, pwm.get_duty_cycle() - 30)  # Zabráníme zápornému duty cycle
    pwm.ChangeDutyCycle(new_duty_cycle)
    
    while True:
        # Vaše kódování nebo čekání
        time.sleep(1)
finally:
    # Zastavíme PWM a vrátíme GPIO do výchozího stavu
    pwm.stop()
    GPIO.cleanup()
