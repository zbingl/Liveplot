import csv
import random
import time
import os
import numpy as np

file_path = 'data.csv'



# Function to generate random values between 0 and 10
random.uniform(0, 10)

# Function to append values to the CSV file
def append_to_csv(file_path, values):
    with open(file_path, 'a', newline='') as csvfile:
        csv.writer(csvfile).writerow(values)


modifiers = ["t"]
for i in range(20):
    modifiers.append(random.randint(1,30))

def main():
    start_time = time.time()
    for i in range(200):
        value = [time.time() - start_time] + [k*np.log(i+1)*(random.random()+6)/7 for k in modifiers[1:]]
        append_to_csv(file_path, value)
        print(f"Random values appended")
        time.sleep(1)

if not os.path.isfile(file_path):
    print(os.path.isfile(file_path))
    with open(file_path, 'w', newline='') as csvfile:
        append_to_csv(file_path, modifiers)
        main()
else:
    print(os.path.isfile(file_path))
    main()


