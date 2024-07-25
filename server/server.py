from flask import Flask, request, jsonify
import util

app = Flask(__name__)

@app.route("/get_location_names")
def get_location_names():
    response = jsonify({
        "location": util.get_location_names()
    })
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    bedrooms = float(request.form['bedrooms'])
    house_type = request.form['house_type']
    parking_space = float(request.form['parking_space'])

    response = jsonify({
        'estimated_price': util.get_estimated_price(bedrooms, parking_space, house_type)
    })

    response.headers.add("Access-Control-Allow-Origin", "*")

    return response

if __name__ == '__main__':
    util.load_saved_artifects()  # Load artifacts before running the application
    app.run(port=5000)  # Run the application on port 5000
