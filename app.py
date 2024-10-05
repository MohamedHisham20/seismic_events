import random
from flask import Flask, request, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from flask_cors import CORS
from obspy import read


def predict_seismic_event(passed_model=None):
    file = request.files['file']
    # try:
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

    predicted_relative_time = 73500  # model output

    # get the date and time of the data start time
    date_time = traces.stats.starttime

    # convert the numpy base64 to string
    date_time_str = str(date_time)

    # split the date and time
    date, time = date_time_str.split('T', 1)

    # remove the z in the time
    time_str = time.split('Z')[0]
    # convert the time into seconds
    seconds = time_to_seconds(time_str)

    # add the time of start of the seismic event
    start_time_seconds = seconds + predicted_relative_time
    # convert back to time (clock)
    start_time_clock = seconds_to_time(start_time_seconds)

    # get the speed of the data at the start time
    speed = tr_data[int(predicted_relative_time)]

    #make speed positive
    speed = abs(speed)

    # randomize the lat and lng of the data

    # the lat between -84 and 77
    lat = random.randint(-84, 77)

    # the lng between -134 and 101
    lng = random.randint(-134, 101)

    # plot the data
    fig, ax = plt.subplots()
    ax.plot(tr_times, tr_data)  # time on x-axis and velocity on y-axis

    # Add the prediction to the plot as a red vertical line
    ax.axvline(x=predicted_relative_time, color='r', linestyle='--')

    # Convert the plot to an image in memory
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Encode the image in base64
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')

    return {'image': image_base64, 'speed': speed, 'lat': lat, 'lng': lng, 'date': date, 'time': start_time_clock}


def time_to_seconds(time_str):
    if isinstance(time_str, str):  # Check if the input is a string
        # Split the time string into parts
        h, m, s = time_str.split(':')

        # If seconds contain fractional seconds, split them
        if '.' in s:
            s, ms = s.split('.')  # Split seconds into whole and fractional parts
        else:
            ms = '0'  # Set milliseconds to zero if not present

        # Convert to integer
        return int(h) * 3600 + int(m) * 60 + int(s) + float('0.' + ms)  # Include milliseconds as seconds
    else:
        raise ValueError("Input must be a string in the format 'HH:MM:SS'")


# Function to convert seconds to time string
def seconds_to_time(seconds):
    hours = seconds // 3600  # Get total hours
    minutes = (seconds % 3600) // 60  # Get total minutes
    secs = seconds % 60  # Get remaining seconds

    # Format the time string
    return f"{int(hours):02}:{int(minutes):02}:{int(secs):02}"


app = Flask(__name__)
CORS(app)

# Set maximum upload size to 100 MB
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB


# landing page
@app.route('/')
def index():
    return 'Welcome to the landing page'


# Route to handle file upload in mseed format
@app.route('/upload_mseed_lunar', methods=['POST'])
def upload_mseed_file_lunar():
    # Check if the file is in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    try:
        final_dict = predict_seismic_event()
        return jsonify(final_dict), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    #return the image to the user in form of png

    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500


# Route to handle file upload in mseed format for mars
@app.route('/upload_mseed_mars', methods=['POST'])
def upload_mseed_file_mars():
    # Check if the file is in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    try:
        final_dict = predict_seismic_event()
        return jsonify(final_dict), 200

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

        start_time = 12720  # model output

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
