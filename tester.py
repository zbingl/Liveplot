import random
import time
import sqlite3
import os
import numpy as np

dataFileName = "data.db"

# Initial table creation
def init():
    if not os.path.exists(dataFileName):
        print(f"The file {dataFileName} does not exist, creating it now.")
    else:
        print(f"The file {dataFileName} exists, proceeding with initialization.")

    try:
        with sqlite3.connect(dataFileName) as connection:
            cursor = connection.cursor()
            create_table_query = """
                CREATE TABLE IF NOT EXISTS data (
                    time REAL PRIMARY KEY,
                    v1 REAL DEFAULT 0,
                    v2 REAL DEFAULT 0,
                    v3 REAL DEFAULT 0,
                    v4 REAL DEFAULT 0
                )
            """
            cursor.execute(create_table_query)
    except sqlite3.Error as e:
        print(f"Error occurred while initializing the database: {e}")



# Empties the CSV file
def clear_all():
    with sqlite3.connect(dataFileName) as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM data")



# Returns a list of datapoints, with the first value being a timestamp
def add_new_vals(start_time) :
    with sqlite3.connect(dataFileName) as connection:
        cursor = connection.cursor()

        t = round(time.time() - start_time, 2)
        value1 = np.abs((np.sin((2*np.pi*time.time())/30)))
        value2 = (np.sin((2*np.pi*time.time())/10))
        value3 = (np.cos((2*np.pi*time.time())/10))
        value4 = float(random.randint(-1,5))

        cursor.execute("INSERT INTO data (time, v1, v2, v3, v4) VALUES (?, ?, ?, ?, ?)", 
                    (t, value1, value2, value3, value4))
        
        print("5 new values appended")


def main():
    init()
    clear_all()
    start_time = time.time()
    for i in range(200):
        add_new_vals(start_time)
        time.sleep(1)
    

if __name__ == "__main__":
    main()


