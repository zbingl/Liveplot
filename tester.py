import random
import time
import numpy as np
import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS data (
        time INTEGER PRIMARY KEY,
        v1 REAL DEFAULT 0,
        v2 REAL DEFAULT 0,
        v3 REAL DEFAULT 0,
        v4 REAL DEFAULT 0
    )
""")


# Empties the CSV file
def clear_all():
    cursor.execute("DELETE FROM data")

# Returns a list of datapoints, with the first value being a timestamp
def add_new_vals(start_time) :
        value1 = round(time.time() - start_time, 1)
        value2 = np.abs((np.sin((2*np.pi*time.time())/30)))
        value3 = (np.sin((2*np.pi*time.time())/10))
        value4 = (np.cos((2*np.pi*time.time())/10))
        value5 = random.randint(-1,5)

        cursor.execute("INSERT INTO data (time, v1, v2, v3, v4) VALUES (?, ?, ?, ?, ?)", 
                       (value1, value2, value3, value4, value5))



def main():
    start_time = time.time()
    for i in range(200):
        add_new_vals(start_time)

        cursor.execute("SELECT MAX(time) FROM data")
        largest_id = cursor.fetchone()[0]
        cursor.execute("SELECT * FROM data WHERE time = ?", (largest_id,))
        added_vals = cursor.fetchall()[0]

        print(f"{len(added_vals)} new values appended")

        time.sleep(1)
    connection.close()

if __name__ == "__main__":
    main()


