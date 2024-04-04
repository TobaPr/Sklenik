from i2clcd import I2cLcd
import board

i2c = board.I2C()  # uses board.SCL and board.SDA


#lcd = i2clcd.i2clcd(i2c_bus=1, i2c_addr=0x3f, lcd_width=20)
lcd = I2cLcd(i2c, 0x3f, 4, 20) 
lcd.init()

lcd.clear()

# Zobraz text na displeji
lcd.move_to(0, 0)
lcd.putstr("Hello, world!")
