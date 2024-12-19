import csv
import random
import time
import os
import numpy as np

FILE_PATH = 'data.csv'


# Function to append values to the CSV file
def append_to_csv(file_path, values):
    with open(file_path, 'a', newline='') as csvfile:
        csv.writer(csvfile).writerow(values)

def createValues(i, start_time) :
        value1 = i
        #value2 = (time.time() - start_time) + (np.log(i+1)*(random.random()+6)/7)
        value3 = (np.sin((2*np.pi*time.time())/10))
        value4 = (np.cos((2*np.pi*time.time())/10))

        return [value1, value3, value4]

def initialize_csv(file_path):
    if not os.path.isfile(file_path):
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Write header row for clarity
            writer.writerow(['Value1', 'Value2', 'Value3'])
        print(f"Initialized new CSV file at {file_path}")

def main(file_path):
    initialize_csv(file_path)
    start_time = time.time()

    for i in range(200):
        values = createValues(i, start_time)
        append_to_csv(file_path, values)
        print("{} new values appended".format(len(values)))
        time.sleep(1)

if __name__ == "__main__":
    main(FILE_PATH)


