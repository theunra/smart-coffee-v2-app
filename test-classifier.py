from lib.roast_classifier.predict import Predict
import pandas as pd

predictor = Predict()

# df = pd.read_csv("./data/kamis-21-maret/enose_raw_datas_202403221033.csv")
df = pd.read_csv("./data/kamis-21-maret/enose_raw_datas_202403221039-1711078768711.csv")


mq_135 = df['adc_mq135'].to_list()
mq_136 = df['adc_mq136'].to_list()
mq_137 = df['adc_mq137'].to_list()
mq_138 = df['adc_mq138'].to_list()
mq_2 = df['adc_mq2'].to_list()
mq_3 = df['adc_mq3'].to_list()
tgs_2620 = df['adc_tgs822'].to_list()


data_to_predict = []
results = []


# for i in range(0, len(mq_135)):
#     data_to_predict.append(mq_135[i])
#     data_to_predict.append(mq_137[i])
#     data_to_predict.append(mq_138[i])
#     data_to_predict.append(mq_3[i])

#     if(len(data_to_predict) >= 100):
#         prediction = predictor.predict(data_to_predict)
#         results.append(prediction)

#         data_to_predict = data_to_predict[12:100]

for i in range(0, len(mq_135)):
    data = []
    data.append(mq_135[i])
    data.append(mq_136[i])
    data.append(mq_137[i])
    data.append(mq_138[i])
    data.append(mq_2[i])
    data.append(mq_3[i])
    data.append(tgs_2620[i])

    data_to_predict.append(data)

    prediction = predictor.predict(data_to_predict)
    results.append(prediction)

    if(len(data_to_predict) > 10):
        data_to_predict = data_to_predict[1:10]

print(results)