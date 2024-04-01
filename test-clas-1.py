import numpy as np
import joblib
import pandas as pd

def load_knn_model(model_filename='knn_model.joblib'):
    knn_model = joblib.load(model_filename)
    return knn_model

# Prediction class
# Class 0 => Unclass
# Class 1 => Light
# Class 2 => Medium
# Class 3 => Dark

input_array = []
predictions = 0
last_prediction = 0

# Real-time input_array
def make_predictions(input_array, knn_model):
    global predictions, last_prediction
    
    input_array = np.array(input_array).reshape(1, -1)  # Reshape to a 2D array
    predictions = knn_model.predict(input_array)
    if last_prediction > predictions:
        last_prediction = predictions
    return predictions

def convert(predictions):
    if predictions == 0:
        return 'Unclass'
    elif predictions == 1:
        return 'Light'
    elif predictions == 2:
        return 'Medium'
    elif predictions == 3:
        return 'Dark'
    

###############################################################
##############################################################
###############################################################


#ambil data
df = pd.read_csv("./data/kamis-21-maret/enose_raw_datas_202403221039-1711078768711.csv")

mq_135 = df['adc_mq135'].to_list()
mq_136 = df['adc_mq136'].to_list()
mq_137 = df['adc_mq137'].to_list()
mq_138 = df['adc_mq138'].to_list()
mq_2 = df['adc_mq2'].to_list()
mq_3 = df['adc_mq3'].to_list()
tgs_822 = df['adc_tgs822'].to_list()
tgs_2620 = df['adc_tgs2620'].to_list()

#load ai
knn_model = load_knn_model("svm_model.joblib")


#predict
data_to_predict = []
for i in range(0, len(mq_135)):
    data_to_predict.append(mq_135[i])
    data_to_predict.append(mq_137[i])
    data_to_predict.append(mq_138[i])
    data_to_predict.append(mq_3[i])

    input_array = data_to_predict

    if(len(input_array) < 100):
        continue

    num_predictions = make_predictions(input_array, knn_model)
    predictions = convert(num_predictions)

    #shift data
    data_to_predict = data_to_predict[8:100]

print("Predictions:", predictions)