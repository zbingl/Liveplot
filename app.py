import csv
import base64
import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, render_template, Response, send_file
from io import BytesIO
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from matplotlib.figure import Figure




app = Flask(__name__)
dataFileName = 'data.csv'

# Reads data from CSV file
def read_csv(file_path):
    columns = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)
        num_columns = len(headers)
        
        for _ in range(num_columns):
            columns.append([])

        for row in csv_reader:
            for i in range(num_columns):
                columns[i].append(float(row[i]))
    return columns

# Generates placeholder image while datafile is empty as a Base64 string
def generate_placeholder_plot():
    fig = Figure(figsize=(18, 8))
    ax = fig.subplots()
    ax.text(0.5, 0.5, "No Data Available", fontsize=20, ha='center', va='center', alpha=0.6)
    ax.axis('off')
    buf = BytesIO()
    fig.savefig(buf, format="png")
    return f'data:image/png;base64,{base64.b64encode(buf.getbuffer()).decode("ascii")}'

# Generates a plot image as a Base64 string
def generate_plot(columns):
    if not columns or all(len(col) == 0 for col in columns):
        return generate_placeholder_plot()


    fig = Figure(figsize=(18, 8))
    ax = fig.subplots()

    start, end = columns[0][0], columns[0][-1]
    ax.xaxis.set_ticks(np.linspace(start, end, 10))
    ax.set_ylabel("Measured Data")
    ax.set_xlabel("Time (s)")

    for j in range(1, len(columns)):
        ax.plot(columns[0], columns[j], marker='o')

    buf = BytesIO()
    fig.savefig(buf, format="png")

    return f'data:image/png;base64,{base64.b64encode(buf.getbuffer()).decode("ascii")}'


# Initial data
try:
    data = generate_plot(read_csv(dataFileName))
except Exception as e:
    print(f"Error initializing data: {e}")
    data = None

# Watchdog event handler
class CSVHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.csv'):
            global data
            try:
                data = generate_plot(read_csv(dataFileName))
                print("Data updated.")
            except Exception as e:
                print(f"Error updating data: {e}")

# Flask routes
@app.route('/')
def index():
    try:
        columns = read_csv(dataFileName)
        plot = generate_plot(columns)
    except:
        print("Error")
        plot = generate_placeholder_plot()
    return render_template('index.html', data=plot,)

@app.route('/get_image')
def get_image():
    try:
        columns = read_csv(dataFileName)
        return generate_plot(columns)
    except :
        print("Error")
        return generate_placeholder_plot()
    
@app.route('/get_file_name')
def get_file_name():
    return dataFileName
    

# Start Watchdog observer
if __name__ == '__main__':

    event_handler = CSVHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()

    try:
        app.run(debug=True, use_reloader=False)
    finally:
        observer.stop()
        observer.join()
