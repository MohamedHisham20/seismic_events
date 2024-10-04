from flask import Flask, request, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Route to handle file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the file is in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']  # The CSV file
    try:
        # Read the CSV file into a pandas DataFrame
        data = pd.read_csv(file)

        # Here you would run your regression model or any other processing
        # For demonstration, let's create a simple plot based on the CSV data
        # Assuming your CSV has columns 'x' and 'y'

        # Example regression logic (replace this with your model)
        # prediction = your_regression_model(data)

        start_time = 12720     # model output

        # plot the data
        fig, ax = plt.subplots()
        ax.plot(data['time_rel(sec)'], data['velocity(m/s)'])  #time on x-axis and velocity on y-axis

        # Add the prediction to the plot as a red vertical line
        ax.axvline(x=start_time, color='r', linestyle='--')

        # Convert the plot to an image in memory
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        # Encode the image in base64
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')

        #return the image to the user in form of png
        return jsonify({'image': image_base64}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
