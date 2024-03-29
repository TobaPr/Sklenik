import board
import busio

# Inicializace I2C sběrnice
i2c = busio.I2C(board.SCL, board.SDA)

# Zobrazení seznamu zařízení na I2C sběrnici
print("Seznam zařízení na I2C sběrnici:")
for device in i2c.scan():
    print(hex(device))
