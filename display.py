import board
import busio
import time

from adafruit_character_lcd import character_lcd_i2c

# Inicializace I2C sběrnice
i2c = busio.I2C(board.SCL, board.SDA)



# Inicializace objektu LCD s I2C adresou 0x27
#lcd = character_lcd.Character_LCD_I2C(i2c, lcd_columns, lcd_rows, address=0x3f)
lcd = character_lcd_i2c.Character_LCD_I2C(i2c, 20, 4, address=0x3f)

# Zapnutí LCD displeje
lcd.backlight = True

# Nastavení jasu na 100 %
lcd.brightness = 1.0

# Výpis textu na displej
lcd.message = "Hello\nworld!"

# Pauza
time.sleep(2)

# Výpis dalšího textu na displej
lcd.message = "Raspberry Pi\nLCD test"