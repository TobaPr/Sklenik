import RPi.GPIO as GPIO
import serial
import time

RESET_PIN = 17  # předpokládáme, že PA13 (RESET) je připojen na GPIO17

# Reset modulu
GPIO.setmode(GPIO.BCM)
GPIO.setup(RESET_PIN, GPIO.OUT)

print("Resetuji RAK811...")
GPIO.output(RESET_PIN, GPIO.LOW)
time.sleep(0.2)
GPIO.output(RESET_PIN, GPIO.HIGH)
time.sleep(1)  # počkej až naběhne

# Zkus poslat AT příkaz
ser = serial.Serial("/dev/serial0", baudrate=115200, timeout=2)
ser.write(b"AT\r\n")
time.sleep(0.5)
response = ser.read_all()

print("Odpověď z modulu:")
print(response.decode(errors="ignore"))

ser.close()
GPIO.cleanup()
