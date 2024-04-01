import numpy as np
import joblib
import os

class Predict:
    '''
    Prediction class
    Class 0 => Unclass
    Class 1 => Light
    Class 2 => Medium
    Class 3 => Dark
    '''

    def __init__(self) -> None:
        self.predictions = None # [.] -> 'Unclass' , 'Light' , 'Medium' , 'Dark'
        self.last_prediction = 0
        self.model = None
        self.load_model()

    def load_model(self):
        package_directory = os.path.dirname(os.path.abspath(__file__))
        model_filename = package_directory + '/model/svmodel.joblib'
        self.model = joblib.load(model_filename)
    
    # Real-time input_array
    def make_predictions(self, input_array):
        # input_array = np.array(input_array).reshape(1, -1)  # Reshape to a 2D array
        # print(input_array)
        self.predictions = self.model.predict(input_array)

    def convertFromIdx(self, prediction):
        if prediction == 0:
            return 'unclass'
        elif prediction == 1:
            return 'light'
        elif prediction == 2:
            return 'medium'
        elif prediction == 3:
            return 'dark'
    
    def convertToIdx(self, prediction):
        if prediction == 'unclass':
            return 0
        elif prediction == 'light':
            return 1
        elif prediction == 'medium':
            return 2
        elif prediction == 'dark':
            return 3
    
    def resetPredict(self):
        self.last_prediction = 0

    def predict(self, input_array) -> str:
        """
        @return predictions
        """
        self.make_predictions(input_array)
        
        pred = self.predictions[0]
        pred = self.convertToIdx(pred)
        
        if(self.last_prediction + 1 == pred):
            self.last_prediction = pred
        
        # print("Predictions:", self.predictions)
        # print("Last prediction : ", self.last_prediction)

        return self.convertFromIdx(self.last_prediction)