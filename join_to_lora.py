#!/usr/bin/env python3
# V3.0.x firmware
from rak811.rak811_v3 import Rak811

# test xxx
lora = Rak811()
lora.hard_reset()
lora.set_config('lora:work_mode:0')
lora.set_config('lora:join_mode:0')
lora.set_config('lora:region:EU868')
lora.set_config('lora:app_eui:AC1F09FFF8680811')
lora.set_config('lora:app_key:AC1F09FFFE03DD04AC1F09FFF8680811')
lora.set_config('lora:dr:5')
lora.join()
lora.send('Hello world')
while lora.nb_downlinks:
            print('Downlink received', lora.get_downlink()['data'].hex())
lora.close()