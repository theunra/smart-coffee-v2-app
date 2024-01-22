from lib.roast_classifier.predict import Predict
from lib.enose.serial_handler import SerialHandler

def testPrediction():
    predictor = Predict()
    
    port = SerialHandler.findPort("ESP32")
    
    print("[Enose] Connecting to serial port : " + port.device)
    serialHandler = SerialHandler(port=port.device, baud=115200)

    serialHandler.startListening()

    # datas = [[22378, 3033, 20534, 18928, 15281, 23270, 23224, 24024, 22378, 3033, 20534, 18928, 15281, 23270, 23224, 24024, 22378, 3033, 20534, 18928, 15281, 23270, 23224, 24024, 22378, 3033, 20534, 18928, 15281, 23270, 23224, 24024, 22378, 3033, 20534, 18928, 15281, 23270, 23224, 24024, 22378, 3033, 20534, 18928, 15281, 23270, 23224, 24024, 22378, 3033, 20534, 18928, 15281, 23270, 23224, 24024, 22378, 3033, 20534, 18928, 15281, 23270, 23224, 24024, 22378, 3033, 20534, 18928, 15281, 23270, 23224, 24024, 22378, 3033, 20534, 18928, 15281, 23270, 23224, 24024, 22378, 3033, 20534, 18928, 15281, 23270, 23224, 24024, 22378, 3033, 20534, 18928, 15281, 23270, 23224, 24024, 22378, 3033, 20534, 18928],]

    # predictor.predict(datas[len(datas) - 1])