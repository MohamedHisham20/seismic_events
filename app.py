from flask import Flask, request, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from flask_cors import CORS
from obspy import read

app = Flask(__name__)
CORS(app)

# Set maximum upload size to 100 MB
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB

#landing page
@app.route('/')
def index():
    return 'Welcome to the landing page'



# Route to handle file upload in mseed format
@app.route('/upload_mseed_lunar', methods=['POST'])
def upload_mseed_file_lunar():
    # Check if the file is in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    try:
        # Read the mseed file into a pandas DataFrame
        mseed_data = read(file)
        traces = mseed_data.traces[0].copy()
        tr_times = traces.times()
        tr_data = traces.data
        # Here you would run your regression model or any other processing
        # For demonstration, let's create a simple plot based on the CSV data
        # Assuming your CSV has columns 'x' and 'y'

        # Example regression logic (replace this with your model)
        # prediction = your_regression_model(data)

        start_time = 12720     # model output

        # get the speed of the data at the start time
        speed = tr_data[int(start_time)]

        # plot the data
        fig, ax = plt.subplots()
        ax.plot(tr_times, tr_data)  #time on x-axis and velocity on y-axis

        # Add the prediction to the plot as a red vertical line
        ax.axvline(x=start_time, color='r', linestyle='--')

        # Convert the plot to an image in memory
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        # Encode the image in base64
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')

        #return the image to the user in form of png
        return jsonify({'image': image_base64, 'speed':speed}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to handle file upload in mseed format for mars
@app.route('/upload_mseed_mars', methods=['POST'])
def upload_mseed_file_mars():
    # Check if the file is in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    try:
        # Read the mseed file into a pandas DataFrame
        mseed_data = read(file)
        traces = mseed_data.traces[0].copy()
        tr_times = traces.times()
        tr_data = traces.data
        # Here you would run your regression model or any other processing
        # For demonstration, let's create a simple plot based on the CSV data
        # Assuming your CSV has columns 'x' and 'y'

        # Example regression logic (replace this with your model)
        # prediction = your_regression_model(data)

        start_time = 12720     # model output

        # get the speed of the data at the start time
        speed = tr_data[int(start_time)]

        # plot the data
        fig, ax = plt.subplots()
        ax.plot(tr_times, tr_data)  #time on x-axis and velocity on y-axis

        # Add the prediction to the plot as a red vertical line
        ax.axvline(x=start_time, color='r', linestyle='--')

        # Convert the plot to an image in memory
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        # Encode the image in base64
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')

        #return the image to the user in form of png
        return jsonify({'image': image_base64, 'speed':speed}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to handle csv files
@app.route('/upload_csv_lunar', methods=['POST'])
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
    app.run(debug=True, port=2003)
