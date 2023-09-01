from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)
MODELS_PATHS = {'regression': "models/reg_model.pkl",
                'binary_classification': 'models/binay_classification_model.pkl'}


def model_loading(model_name):
    """
       Load a pre-trained machine learning model from a pickle file.

       Parameters:
       - model_name (str): The name of the model to load.

       Returns:
       - model: The loaded machine learning model.
    """
    # Load the pre-trained model from the pickle file
    model_path = MODELS_PATHS.get(model_name)
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    return model


@app.route('/')
def index():
    """
        Render the index.html template.

        Returns:
        - str: HTML content to be displayed in the browser.
    """
    return render_template("index.html")


def get_data():
    """
        Extract input data from a JSON request and convert it into a 2D array of features.

        Returns:
        - input_features (numpy.ndarray): A 2D array of input features.
        - model_type (str): The type of the machine learning model to be used.
    """
    # Get input data from the JSON request
    data = request.get_json()

    # Extract numerical features from the JSON data
    features = [
        data['Medu'], data['Fedu'], data['failures'], data['goout'],
        data['Dalc'], data['Walc'], data['absences'], data['G1'],
        data['G2'], data['address_U'], data['Mjob_health'],
        data['Mjob_other'], data['Fjob_teacher'], data['schoolsup_yes']
    ]

    # Convert the input features to a 2D array for prediction
    input_features = np.array([features])
    return input_features, data['model_type']


@app.route('/predict', methods=['POST'])
def predict():
    """
        Make predictions using a loaded machine learning model and return the results as JSON.

        Returns:
        - jsonify: A JSON response containing the model's prediction or an error message.
    """
    try:

        input = get_data()
        input_features = input[0]
        model = model_loading(input[1])
        # Make a prediction using the loaded model
        prediction = model.predict(input_features)

        if input[1] == 'regression':
            # Return the prediction as JSON response
            response = {'prediction': int(prediction[0])}
            return jsonify(response), 200
        else:
            # Return the prediction as JSON response
            response = {'prediction': prediction[0]}
            return jsonify(response), 200
    except Exception as e:
        error_message = str(e)
        return jsonify({'error': error_message}), 400


if __name__ == '__main__':
    app.run()
