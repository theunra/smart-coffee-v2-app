from lib.roast_classifier.predict import Predict
from lib.enose.serial_handler import SerialHandler

def onSerialDataReceive(data):
    print(data)

def testListenSerialData():
    port = SerialHandler.findPort("ESP32")

    print("[Enose] Connecting to serial port : " + port.device)
    serialHandler = SerialHandler(port=port.device, baud=115200)

    serialHandler.startListening(target=onSerialDataReceive)