import json
from flask import Flask, request, jsonify
import pandas as pd
import pickle
import  numpy as np
__locations  = None
__data_columns = None
__model = None


def get_estimated_price(bedrooms, parking_space, house_type):
    try:
        # Convert house_type to lowercase
        house_type = house_type

        # Create a DataFrame with the input data
        df = pd.DataFrame({
            "bedrooms": [bedrooms],
            "parking_space": [parking_space],
            "house_type": [house_type]
        })

        # Perform one-hot encoding on the 'house_type' column
        df_encoded = pd.get_dummies(df)

        try:
            # Load the trained model
            with open('artifacts/lekki_home_prices_model.pickle', 'rb') as file:
                model = pickle.load(file)

            # Load the X_train dataframe
            with open('artifacts/x_train.pickle', 'rb') as file:
                X_train = pickle.load(file)

            # Get the column names from the training data used for the model
            model_columns = X_train.columns.to_list()

            # Ensure the encoded dataframe has the same columns as the training data
            df_encoded = df_encoded.reindex(columns=model_columns, fill_value=0)

            # Make the prediction using the loaded model
            prediction = model.predict(df_encoded).round(2)[0]

            formatted_prediction = "₦{:,}".format(prediction)
            # Prepare the response
            response = {
                "prediction": formatted_prediction
            }

            return (response)

        except FileNotFoundError:
            error_response = {
                "error": "Model or X_train pickle file not found"
            }
            return jsonify(error_response), 500

    except KeyError:
        error_response = {
            "error": "Invalid input format"
        }
        return jsonify(error_response), 400

def get_location_names():
    return __locations


def load_saved_artifects():
    print("loading saved artifacts .. start")
    global __data_columns
    global __locations

    with open("./artifacts/columnsX_train.json",'r') as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[2:]

    global __model

    with open("./artifacts/lekki_home_prices_model.pickle","rb") as f:
        __model = pickle.load(f)

    print("loading saved artifects..done")
if __name__ == '__main__':
    load_saved_artifects()
    print(get_location_names())
    print(get_estimated_price(4, 3, "Block of Flats"))
    print(get_estimated_price(4, 3, "Detached Duplex"))
    print(get_estimated_price(4, 3, "Semi Detached Duplex"))
    print(get_estimated_price(4, 1, "Block of Flats"))

