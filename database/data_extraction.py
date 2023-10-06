from word2number import w2n

def read_file():

    """
    Reads weather data from a text file and returns it as a list of strings.

    Returns:
        list: A list where each element is a line from the file.
    """
    with open('weather-data.txt', 'r') as file:
        return file.readlines()


def handled_data(data):

    """
    Handle missing or inconsistent data in the weather data.

    Args:
        data (list): List of strings, each containing a data record.

    Returns:
        list: List of modified data with missing or inconsistent values replaced.
    """

    missing_value_replaced_rows = []
 
    for line in data:
        parts = line.strip().split(',')
        if len(parts) == 5:
            date, city, temperature, humidity, condition = map(str.strip, parts)

            if temperature == "":
                temperature = -1
            if humidity == "":
                humidity = -1
            if condition == "":
                condition = 'Sunday'
            if city == "":
                city = 'Durban'

            modified_line = f"{date}, {city}, {temperature}, {humidity}, {condition}\n"
            missing_value_replaced_rows.append(modified_line)

    return missing_value_replaced_rows


def convert_to_fahrenheit(celsius):

    """
    Convert temperature in Celsius to Fahrenheit.

    Args:
        celsius (str): Temperature in Celsius.

    Returns:
        str: Temperature in Fahrenheit.
    """


    if celsius == "null":
        return "null"
    else:
        celsius = int(celsius)
        fahrenheit = (celsius * 9/5) + 32
        return fahrenheit
    


def determine_weather_type(temperature):

    """
    Determine the weather type based on temperature in Fahrenheit.

    Args:
        temperature (str): Temperature in Fahrenheit.

    Returns:
        str: Weather type ('Warm', 'Cold', 'Moderate', or 'null' for missing values).
    """

    if temperature == "null":
        return "null"
    elif temperature > 75:
        return "Warm"
    elif temperature < 59:
        return "Cold"
    else:
        return "Moderate"

def convert_to_number(value):

    """
    Converts a number written in words (string or word) to an integer.

    Args:
        value (str): Numeric value as a string.

    Returns:
        int or None: Integer value if conversion is successful, else None.
    """
    try:
        return int(value)
    except ValueError:
        try:
            return w2n.word_to_num(value)
        except ValueError:
            return None

def add_weather_type_column(data):

    """
    Add a 'weather_type' column to the weather data based on temperature.

    Args:
        data (list): List of strings, each containing a data record.

    Returns:
        list: List of data records with the 'weather_type' column added.
    """

    modified_data = []

    for line in data:
        parts = line.strip().split(',')

        if len(parts) == 5:
            # unpacking of the rows in the data 
            date, city, temperature, humidity, condition = map(str.strip, parts)

            if temperature != "Temperature(C)":
                if temperature.isdigit():
                    temperature_fahrenheit = convert_to_fahrenheit(temperature)
                else:
                    temperature_numeric = convert_to_number(temperature)
                    if temperature_numeric is not None:
                        temperature_fahrenheit = convert_to_fahrenheit(str(temperature_numeric))
                    else:
                        temperature_fahrenheit = None

                weather_type = determine_weather_type(temperature_fahrenheit)

                # adding a a weather_type line in the data and adding it to the list
                modified_line = f"{date}, {city}, {temperature}, {humidity}, {condition}, {weather_type}\n"
                modified_data.append(modified_line)

    return modified_data




def main():
    # we first read the raw data file
    data = read_file()
    # handle the raw data and add a weather_type column 
    modified_data = add_weather_type_column(handled_data(data))
    # turning list elements into tuples, this makes it easier to insert values in database
    processed_data = [tuple(line.strip().split(',')) for line in modified_data]

    return processed_data

if __name__ == '__main__':
    data_to_insert = main()
    print(data_to_insert)

