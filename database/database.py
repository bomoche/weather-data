import sqlite3
import data_extraction as data
import os
import csv

def db_connect(db_file):

    """
    Connect to the SQLite database.

    Args:
        db_file (str): The name of the SQLite database file.

    Returns:
        sqlite3.Connection or None: The database connection or None if the file does not exist.
    """

    if os.path.isfile(db_file):
        return sqlite3.connect(db_file)
    else:
        print(f"The database file '{db_file}' does not exist.")
        return None

def create_table(conn):

    """
    Creates the HistoricalWeatherData table in the database if it doesn't exist.

    Args:
        conn (sqlite3.Connection): The database connection.
    """

    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS HistoricalWeatherData (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            city TEXT,
            temperature INTEGER,
            humidity INTEGER,
            condition TEXT,
            weather_type TEXT
        )
    ''')

def insert_data(conn, weather_data):

    """
    Inserts weather data into the HistoricalWeatherData table.

    Args:
        conn (sqlite3.Connection): The database connection.
        weather_data (list of tuples): Weather data to insert.
    """

    cursor = conn.cursor()
    cursor.executemany('''
        INSERT INTO HistoricalWeatherData (date, city, temperature, humidity, condition, weather_type)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', weather_data)
    conn.commit()

def calculate_average_temp_humidity(conn):


    """
    Calculates and prints the average temperature and humidity for Cape Town.

    Args:
        conn (sqlite3.Connection): The database connection.
    """

    cursor = conn.cursor()
    cursor.execute(f'''
        SELECT temperature, humidity
        FROM HistoricalWeatherData
        WHERE city = 'Cape Town';
    ''')
    queried_data = cursor.fetchall()

    if not queried_data:
        print(f"No data found for the specified city")
    else:
        temperature = 0
        humidity = 0

        for row in queried_data:
            temperature += row[0]
            humidity += row[1]

        num_rows = len(queried_data)

        average_temperature = temperature / num_rows
        average_humidity = humidity / num_rows

        print(f"Average Temperature for Cape Town: {average_temperature}°F")
        print(f"Average Humidity for Cape Town: {average_humidity}%")


def export_to_csv(data, filename):

    """
    Exports data to a CSV file.

    Args:
        data (list of tuples): Data to export.
        filename (str): The name of the CSV file.
    """

    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Date", "City", "Temperature(C)", "Humidity(%)", "Condition", "Weather Type"])
        
        for row in data:
            csv_writer.writerow(row)

def main():
    db_file = 'Weather_TechDB.db'
    conn = db_connect(db_file)

    if conn is not None:
        create_table(conn)
        weather_data = data.main()
        insert_data(conn, weather_data)
        calculate_average_temp_humidity(conn)
        conn.close()

    export_to_csv(weather_data,'filtered_weather_data.csv')
    

if __name__ == '__main__':
    main()
