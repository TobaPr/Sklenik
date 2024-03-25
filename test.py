print ("Posílám zprávu: test")

from rak811.rak811_v3 import Rak811

lora = Rak811()
lora.send('test123',3)
lora.close()