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
        self.last_prediction = None
        self.model = None
        self.load_model()

    def load_model(self):
        package_directory = os.path.dirname(os.path.abspath(__file__))
        model_filename = package_directory + '/model/svm_model.joblib'
        self.model = joblib.load(model_filename)
    
    # Real-time input_array
    def make_predictions(self, input_array):
        input_array = np.array(input_array).reshape(1, -1)  # Reshape to a 2D array
        self.predictions = self.model.predict(input_array)

    # def convert(predictions):
    #     if predictions == 0:
    #         return 'Unclass'
    #     elif predictions == 1:
    #         return 'Light'
    #     elif predictions == 2:
    #         return 'Medium'
    #     elif predictions == 3:
    #         return 'Dark'
    
    def predict(self, input_array):
        self.make_predictions(input_array)
        # predictions = convert(num_predictions)
        print("Predictions:", self.predictions)
        return self.predictions