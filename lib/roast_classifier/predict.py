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

    def convert(self, prediction):
        if prediction == 0:
            return 'Unclass'
        elif prediction == 1:
            return 'Light'
        elif prediction == 2:
            return 'Medium'
        elif prediction == 3:
            return 'Dark'
    
    def convert_(self, prediction):
        if prediction == 'Unclass':
            return 0
        elif prediction == 'Light':
            return 1
        elif prediction == 'Medium':
            return 2
        elif prediction == 'Dark':
            return 3
    
    def predict(self, input_array) -> list:
        """
        @return predictions
        """
        out_arr = []
        self.make_predictions(input_array)
        
        # kurangin indeks hasil prediksi
        for pred in self.predictions:
            out_arr.append(self.convert(self.convert_(pred) - 2))
        self.predictions = out_arr
        
        print("Predictions:", self.predictions)

        return self.predictions