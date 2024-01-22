import requests
from random import randint
from datetime import datetime

api_addr = 'https://sites.saveforest.cloud/data'

payload = {
        "method" : "single",
        "raw_datas" :{
            "time" : datetime.utcnow().isoformat(),
            "adc_mq135" : randint(0, 50),
            "adc_mq136" : 3,
            "adc_mq137" : 13,
            "adc_mq138" : 23,
        "adc_mq2" : 53,
        "adc_mq3" : 53,
        "adc_tgs822" : 12,
        "adc_tgs2620" : 14,
        "temp" : 50,
        "humidity": 32.4,
            }
        }
r = requests.post(api_addr, json=payload)

print(r.url)
print(r.json())

