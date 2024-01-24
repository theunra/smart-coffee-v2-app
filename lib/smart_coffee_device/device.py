import requests
from random import randint
from datetime import datetime
from threading import Thread

from lib.enose.enose import Enose

import time

class SmartCoffeeDevice:
    def __init__(self) -> None:
        self.device_id = "77f04f7b-0ec0-4ce7-b8e7-ff629e90d8c3"
        self.device_api_addr = 'https://sites.saveforest.cloud/device'
        self.data_api_addr =  'https://sites.saveforest.cloud/data'
        self.is_run = True
        self.is_send_data = False
        self.is_connected = False

        self.enose = Enose()
        self.enose.onPredictionDone(target=SmartCoffeeDevice.onEnosePredictionDone, args=(self,))
        
        self.LISTEN_TIMEOUT = 10 #s

        self.DEBUG = True

        self.listenCallback = self.handleEvent

        self.send_data_thread = Thread(target=self.sendDataRoutine)
        self.listen_event_thread = Thread(target=self.listenEventRoutine)

    def start(self):
        status = self.connect()
        if(status == False):
            return
        self.send_data_thread.start()
        self.listen_event_thread.start()
        self.enose.start()

        ## Main loop
        while(1):
            try:
                time.sleep(2)
            except KeyboardInterrupt as e:
                print("[SmartCoffeeDevice] Exiting app...")
                self.is_send_data = False
                self.is_connected = False
                self.is_run = False
                print("[SmartCoffeeDevice] Wait for thread to complete...")
                self.send_data_thread.join()
                self.listen_event_thread.join()
                print("[SmartCoffeeDevice] Stopping enose complete...")
                self.enose.stop()
                print("[SmartCoffeeDevice] exit")
                break
    
    def stop(self):
        self.is_run = False

    def connect(self):
        payload = {
                "param" : "connect",
                "id" : self.device_id
                }
        r = requests.post(self.device_api_addr, json = payload)

        if(r.status_code == 200 and r.json()['status'] == 200):
            print("[SmartCoffeeDevice] Connected to " + r.url)
        else:
            print("[SmartCoffeeDevice] connection to server error , status code : ", r.status_code)
            self.is_connected = False
            return False
        
        self.is_connected = True
        return True

    def listenEvent(self):
        r = requests.get(self.device_api_addr, params = {"param" : "event"}, timeout = self.LISTEN_TIMEOUT)
        if(r.status_code == 504):
            print("[SmartCoffeeDevice] listenEvent : Timeout, retrying")
        elif (r.status_code == 200):
            self.listenCallback(r.json())
        else:
            print("[SmartCoffeeDevice] listenEvent : unhandled")

    def sendSensorData(self, sensordata):
        r = requests.post(self.data_api_addr, json = sensordata)
        if (r.status_code == 200):
            return r.json()
        else:
            print("[SmartCoffeeDevice] sendSensorData : unhandled")

    def onEnosePredictionDone(self, data):
        print("[SmartCoffeeDevice] Prediction done : ", data)

    def handleEvent(self, event):
        try:
            if(event["payload"]["event"]["param"] == "start-roast"):
                print("[SmartCoffeeDevice] handleEvent : Start roasting")
                self.is_send_data = True

            elif(event["payload"]["event"]["param"] == "stop-roast"):
                print("[SmartCoffeeDevice] handleEvent : Stop roasting")
                self.is_send_data = False

        except KeyError as e:
            if self.DEBUG:
                print("[SmartCoffeeDevice] handleEvent KeyError : unhandled event " + str(event))
        
        except Exception as e:
            print("[SmartCoffeeDevice] handleEvent error : unhandled error" + repr(e))
            raise Exception(e)

    def listenEventRoutine(self):
        while(self.is_run):
            self.listenEvent()

    def sendDataRoutine(self):
        adc = 20500

        while(self.is_run):
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

            if(self.is_send_data):
                print("[SmartCoffeeDevice] Send sensor data")
                self.sendSensorData(payload)

                adc = adc + randint(0, 200)
            
            time.sleep(0.6)

    
