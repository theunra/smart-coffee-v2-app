from serial import Serial
from serial.tools.list_ports import comports
from threading import Thread
import json

class SerialHandler:
    def __init__(self, port, baud) :
        self.ser = Serial(port=port, baudrate=baud)
        self.is_run = False

        self.onReceiveData = None
        self.thread_serial_listen = Thread(target=self.__listenSerial)
    
    def __read(self):
        while self.is_run:
            if(self.ser.readable()):
                payload = self.ser.readline()
                data_json = json.loads(payload)

                return data_json
        
    def __write(self, payload):
        if(self.ser.writable()):
            return self.ser.write(payload)
        else:
            return False
        
    def __listenSerial(self):
        while(self.is_run):
            data = self.__read()

            self.onReceiveData(data)
    
    def startListening(self):
        if(self.onReceiveData == None):
            raise Exception("onReceiveData callback is None, must provide function(data)")
        self.is_run = True
        self.thread_serial_listen.start()


    @staticmethod
    def getPorts():
        ports = list(comports())
        return ports
    
    @staticmethod
    def findPort(desc):
        """
        @param desc , string to match/find in port description
        @return port if found, else False
        """
        ports = SerialHandler.getPorts()

        for port in ports:
            if(port.description.find(desc) > -1):
                return port
            
        return False