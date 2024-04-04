
import adafruit_character_lcd.character_lcd_i2c as character_lcd
import board


# Definice velikosti displeje (20 sloupců a 4 řádky)
lcd_columns = 20
lcd_rows = 4

# Inicializace I2C sběrnice

i2c = board.I2C()  # uses board.SCL and board.SDA


# Inicializace objektu LCD s I2C adresou 0x27
lcd = character_lcd.Character_LCD_I2C(i2c, lcd_columns, lcd_rows)

# Vypnutí blikání kurzoru
lcd.blink = False

# Nastavení podsvícení na zelenou
lcd.color = [0, 255, 0]

# Výpis textu na displej
lcd.message = "Hello\nworld!"

# Pauza
time.sleep(2)

# Výpis dalšího textu na displej
lcd.message = "Raspberry Pi\nLCD test"