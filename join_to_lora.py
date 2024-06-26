#!/usr/bin/env python3
# V3.0.x firmware
from rak811.rak811_v3 import Rak811

lora = Rak811()
lora.set_config('lora:work_mode:0')
lora.set_config('lora:join_mode:0')
lora.set_config('lora:region:EU868')
lora.set_config('lora:app_eui:AC1F09FFF8680811')
lora.set_config('lora:app_key:AC1F09FFFE03DD04AC1F09FFF8680811')
lora.join()
lora.set_config('lora:dr:5')
lora.send('Hello world')
lora.close()