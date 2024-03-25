#!/usr/bin/env python3
# V3.0.x firmware
from rak811.rak811_v3 import Rak811

lora = Rak811()
lora.set_config('lora:work_mode:0')
lora.set_config('lora:join_mode:0')
lora.set_config('lora:region:EU868')
lora.set_config('lora:app_eui:70B3D5xxxxxxxxxx')
lora.set_config('lora:app_key:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
lora.join()
lora.set_config('lora:dr:5')
lora.send('Hello world')
lora.close()