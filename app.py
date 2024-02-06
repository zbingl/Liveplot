import csv
import matplotlib.pyplot as plt
from flask import Flask, render_template, Response
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
    ax.plot(x, y, marker='o', linestyle='-', color='b')
    #ax.title('Live Plot from CSV Data')
    #ax.xlabel('X-axis')
    #ax.ylabel('Y-axis')
    #ax.grid(True)
    #ax.tight_layout()
    # Save the plot to a temporary file
    fig.savefig('static/plot.png')


    #fig.savefig(buf, format="png")
    #data = f'data:image/png;base64,{base64.b64encode(buf.getbuffer()).decode("ascii")}'

# Watchdog event handler to detect changes in the CSV file
class CSVHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.csv'):
            generate_plot()

# Route to render the HTML template with the live plot
@app.route('/')
def index():
    return render_template('index.html')

# Route to serve the live plot image
@app.route('/plot.png')
def plot_image():
    return Response(open('static/plot.png', 'rb').read(), mimetype='image/png')



if __name__ == '__main__':
    generate_plot()  # Initial plot generation

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
