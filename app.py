import csv
import matplotlib.pyplot as plt
from flask import Flask, render_template, Response, send_file
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from matplotlib.figure import Figure
from io import BytesIO
import base64

app = Flask(__name__)

# Function to read data from CSV file
def read_csv(file_path):
    columns = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)  # Skip the header row
        num_columns = len(headers)
        
        # Initialize lists for each column
        for _ in range(num_columns):
            columns.append([])

        # Read data into columns
        for row in csv_reader:
            for i in range(num_columns):
                columns[i].append(float(row[i]))
    return columns



# Function to generate Matplotlib plot
def generate_plot():
    columns = read_csv('data.csv')

    fig = Figure(figsize=(18,8))
    ax = fig.subplots()

    ax.set_xticks(columns[0])

    ax.set_ylabel("Measured data (ppm)")
    ax.set_xlabel("Time since start (s)")

    for j in range(len(columns)-1):
        ax.plot(columns[0], columns[j+1], marker='o')
    buf = BytesIO()
    fig.savefig(buf, format="png")
    imdata = f'data:image/png;base64,{base64.b64encode(buf.getbuffer()).decode("ascii")}'
    print("New plot generated")
    return imdata

data = generate_plot()

# Watchdog event handler to detect changes in the CSV file
class CSVHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.csv'):
            data = generate_plot()

# Route to render the HTML template with the live plot
@app.route('/')
def index():
    return render_template('index.html', data = data)

@app.route('/get_image')
def get_image():
    print("getimage")
    return generate_plot()

if __name__ == '__main__':
    # Set up the watchdog observer to monitor changes in the CSV file
    event_handler = CSVHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()

    # Run the Flask app
    app.run(debug=True, use_reloader=False)

    # Stop the watchdog observer when the Flask app is closed
    observer.stop()
    observer.join()
