from lib.enose.enose import Enose
from lib.enose.serial_handler import SerialHandler
from time import sleep

def onPredictDone(datas, predictions):
    print(len(datas), predictions)

enose = Enose('COM3')   
enose.onPredictionDone(onPredictDone)
enose.start()

while(1):
    try:
        sleep(1)
    except KeyboardInterrupt as e:
        break

enose.stop()