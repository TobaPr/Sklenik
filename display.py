import i2clcd


lcd = i2clcd.i2clcd(i2c_bus=1, i2c_addr=0x3f, lcd_width=20)
lcd.init()

lcd.print_line('ahoj', line=0)
lcd.print_line('tome ;)', line=1)

