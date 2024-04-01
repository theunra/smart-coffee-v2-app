import numpy as np
import joblib
import os
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

class PredictLDA:
    '''
    Prediction class
    Class 0 => Unclass
    Class 1 => Light
    Class 2 => Medium
    Class 3 => Dark
    '''

    def __init__(self) -> None:
        self.prediction = 0
        self.last_prediction = 0
        self.svm_model = None
        self.lda_model = None
        self.scaler = None

        self.prediction_dict = {
            'unclass' : 0,
            'light' : 1,
            'medium' : 2,
            'dark' : 3
        }

        self.loadModel()

    def loadModel(self):
        package_directory = os.path.dirname(os.path.abspath(__file__))
        svm_model_filename = package_directory + '/model/svm_model.joblib'
        lda_model_filename = package_directory + '/model/lda_model.joblib'
        self.svm_model = joblib.load(svm_model_filename)
        self.lda_model = joblib.load(lda_model_filename)

    def loadScaler(self):
        self.scaler = MinMaxScaler()

        package_directory = os.path.dirname(os.path.abspath(__file__))
        scaler_data = pd.read_csv(package_directory + '/data/scaler.csv')

        scaler_data = scaler_data.drop(columns=['adc_mq3', 'adc_mq135', 'adc_mq136', 'adc_tgs2620', 'adc_tgs822'])

        numeric_scaler_data = scaler_data.select_dtypes(include=[float, int])

        self.scaler.fit_transform(numeric_scaler_data)
    
    def convertPredictionKeyToIdx(self, key) -> int:
        return self.prediction_dict[key]
    
    def convertPredictionIdxToKey(self, idx) -> str:
        return list(self.prediction_dict.keys())[idx]

    def resetPredict(self):
        self.prediction = 0
        self.last_prediction = 0

    def predict(self, input_array) -> str:
        """
        @return predictions
        """

        # Normalize data using scaler
        normalized = self.scaler.transform(input_array)

        # LDA feature extraction
        features = self.lda_model.transform(normalized)

        # Predict data
        predictions = self.svm_model.predict(features)
        
        # Get prediction and convert to idx
        pred = predictions[0]
        self.prediction = self.prediction_dict[pred]
        
        # Check prediction
        if(self.last_prediction + 1 == self.prediction):
            self.last_prediction = self.prediction

        return self.convertPredictionIdxToKey(self.last_prediction)