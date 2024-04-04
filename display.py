import i2clcd

lcd = i2clcd.i2clcd(i2c_bus=1, i2c_addr=0x3f, lcd_width=20)
lcd.init()

# fill a line by the text
lcd.print_line('hello', line=0)
lcd.print_line('world!', line=1, align='RIGHT')

while True:
    time.sleep(10)  # Zpoždění 1 sekunda