import requests
from random import randint
from datetime import datetime
from threading import Thread
import time

device_api_addr = 'https://sites.saveforest.cloud/device'
data_api_addr =  'https://sites.saveforest.cloud/data'

deviceId = "77f04f7b-0ec0-4ce7-b8e7-ff629e90d8c3"

def connect():
    payload = {
            "param" : "connect",
            "id" : deviceId
            }
    r = requests.post(device_api_addr, json=payload)
    print(r.url)
    print(r.json())

def listenEvent():
    LISTEN_TIMEOUT = 10 #s

    r = requests.get(device_api_addr, params={"param" : "event"}, timeout=LISTEN_TIMEOUT)
    print(r.url)
    if(r.status_code == 504):
        print("Timeout, retrying")
    elif (r.status_code == 200):
        print(r.json())
        return r.json()
    else:
        print("unhandled")

def sendSensorData(sensordata):
    r = requests.post(data_api_addr, json=sensordata)
    print(r.url)
    if (r.status_code == 200):
        print(r.json())
        return r.json()
    else:
        print("unhandled")

isRun = True

isSendData = False

def sendDataRoutine():
    adc = 20500

    while(isRun):
        payload = {
		    "method" : "single",
	        "raw_datas" :{
                "roastId" : 0,
                "roastStatus" : 2,
    	        "time" : datetime.utcnow().isoformat(),
    	        "adc_mq135" : adc,
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

        if(isSendData):
            print("send")
            sendSensorData(payload)

            adc = adc + randint(0, 200)
        
        time.sleep(0.6)

connect()

send_data_thread = Thread(target=sendDataRoutine)
send_data_thread.start()

while(True):

    res = listenEvent()
    
    try:
        if(res["payload"]["event"]["param"] == "start-roast"):
            print("Start roasting")
            isSendData = True
    except Exception as e:
        print(e)

isRun = False
