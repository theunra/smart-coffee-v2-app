import requests
from random import randint
from datetime import datetime
from threading import Thread

from lib.enose.enose import Enose

import time

class SmartCoffeeRoast:
    def __init__(self) -> None:
        self.id = -1
        self.beanType = ''
        self.level = ''

    def fromJSON(self, roast):
        self.id = roast['id']
        self.beanType = roast['beanType']
        self.level = roast['level']

class SmartCoffeeSession:
    def __init__(self) -> None:
        self.reset()

    def reset(self):
        self.id = -1
        self.roastId = None

    def fromJSON(self, roastSession):
        self.id = roastSession['id']
        self.roastId = roastSession['roastId']

class SmartCoffeeDevice:
    def __init__(self, serial_port=None) -> None:
        self.device_id = "77f04f7b-0ec0-4ce7-b8e7-ff629e90d8c3"
        self.api_addr = 'https://smartcoffee.saveforest.cloud'
        self.device_api_addr = self.api_addr + '/device'
        self.data_api_addr =  self.api_addr + '/data'
        self.is_run = True
        self.is_send_data = False
        self.is_connected = False

        self.session = SmartCoffeeSession()
        self.roast = SmartCoffeeRoast()

        self.enose = Enose(port=serial_port)
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
                print("[SmartCoffeeDevice] Stopping enose complete...")
                self.enose.stop()
                print("[SmartCoffeeDevice] Wait for thread to complete...")
                self.send_data_thread.join()
                self.listen_event_thread.join()
                print("[SmartCoffeeDevice] exit")
                break
    
    def stop(self):
        self.is_run = False

    def connect(self):
        payload = {
            "key" : "connect",
            "id" : self.device_id
        }
        r = requests.post(self.device_api_addr, json = payload)

        if(r.status_code == 200 and r.json()['status'] == 200):
            print("[SmartCoffeeDevice] Connected to " + r.url)
            roastSession = r.json()["payload"]['roastSession']
            self.session.fromJSON(roastSession)
            if(self.session.roastId == None):
                print("[SmartCoffeeDevice] No session")
        else:
            print("[SmartCoffeeDevice] connection to server error , status code : ", r.status_code)
            self.is_connected = False
            return False
        
        self.is_connected = True
        return True
    
    def getSession(self):
        payload = {
            "key" : "roast-session",
            "id" : self.device_id
        }
        r = requests.get(self.device_api_addr, params = payload)

        if(r.status_code == 200):
            roastSession = r.json()['payload']['roastSession']
            print("[SmartCoffeeDevice] Get session : ", roastSession)

            self.session.fromJSON(roastSession)

            if(roastSession['roastId'] != None):
                roast = r.json()['payload']['roast']
                print("[SmartCoffeeDevice] Get roast : ", roast)
                self.roast.fromJSON(roast)
            
            return True
        
        else:
            print("[SmartCoffeeDevice] Get roast session error : ", r)
            return False

    def listenEvent(self):
        r = requests.get(self.device_api_addr, params = {"key" : "event"})
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

    def onEnosePredictionDone(self, data, predictions):
        print("[SmartCoffeeDevice] Prediction done : ", len(data), predictions)

    def handleEvent(self, event):
        try:
            ev = event["payload"]["event"]["key"]
            if(ev == "start-roast"):
                print("[SmartCoffeeDevice] handleEvent : Start roasting")
                self.is_send_data = True

            elif(ev == "stop-roast"):
                print("[SmartCoffeeDevice] handleEvent : Stop roasting")
                self.is_send_data = False
            
            elif(ev == "create-session"):
                print("[SmartCoffeeDevice] handleEvent : New session created")
                self.getSession()

            elif(ev == "finish-session"):
                print("[SmartCoffeeDevice] handleEvent : session finished")
                self.session.reset()

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
        while(self.is_run):
            if(self.is_send_data):
                self.__sendDummy()
            
            time.sleep(0.1)

    def sendDataBulk(self, datas):
        payload = {
            "method" : "bulk",
            "raw_datas" : datas
        }

        self.sendSensorData(payload)
    """
    DUMMY
    """
    adc = 20500
    status = 0
    count = 0

    def __sendDummy(self):
        SmartCoffeeDevice.adc 
        SmartCoffeeDevice.status
        SmartCoffeeDevice.count

        if(self.session.roastId == None or self.session.roastId < 1):
            print("[SmartCoffeeDevice] invalid session id")
            return
        
        SmartCoffeeDevice.count = SmartCoffeeDevice.count + 1

        SmartCoffeeDevice.status = int(SmartCoffeeDevice.count / 100)

        if(SmartCoffeeDevice.status > 4):
            SmartCoffeeDevice.status = 4
        
        payload = {
            "method" : "single",
            "raw_datas" :{
                "roastId" : self.session.roastId,
                "roastStatus" : SmartCoffeeDevice.status,
                "time" : datetime.utcnow().isoformat(),
                "adc_mq135" : SmartCoffeeDevice.adc,
                "adc_mq136" : SmartCoffeeDevice.adc - 2500,
                "adc_mq137" : SmartCoffeeDevice.adc - 2500 * 2,
                "adc_mq138" : SmartCoffeeDevice.adc - 2500 * 3,
                "adc_mq2" : SmartCoffeeDevice.adc - 2500 * 4,
                "adc_mq3" : SmartCoffeeDevice.adc - 2500 * 5,
                "adc_tgs822" : SmartCoffeeDevice.adc - 2500 * 6,
                "adc_tgs2620" : SmartCoffeeDevice.adc - 2500 * 7,
                "temp" : 50,
                "humidity": 32.4,
            }
        }

        print("[SmartCoffeeDevice] Send sensor data")
        self.sendSensorData(payload)

        SmartCoffeeDevice.adc = SmartCoffeeDevice.adc + randint(0, 200)
    
