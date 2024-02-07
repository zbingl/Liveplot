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
def read_csv(filename='data.csv'):
    x_vals, y_vals = [], []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            x_vals.append(float(row[0]))
            y_vals.append(float(row[1]))
    return x_vals, y_vals







# Function to generate Matplotlib plot
def generate_plot():
    x, y = read_csv()
    fig = Figure()
    ax = fig.subplots()
    ax.plot(x, y, marker='o', linestyle='-', color='g')
    #fig.savefig('static/plot.png')
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
    print("hej")
    return generate_plot()

if __name__ == '__main__':
    generate_plot()
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
