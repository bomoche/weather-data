from word2number import w2n


def read_file():
    with open('weather-data.txt', 'r') as file:
        return file.readlines()


def convert_to_fahrenheit(celsius):
    if celsius == "null":
        return "null"
    else:
        celsius = int(celsius)
        fahrenheit = (celsius * 9/5) + 32
        return fahrenheit

def determine_weather_type(temperature):

    if temperature == "null":
        return "null"
    elif temperature > 75:
        return "warm"
    elif temperature < 59:
        return "cold"
    else:
        return "moderate"

def convert_to_number(value):
    try:
        return int(value)
    except ValueError:
        try:
            return w2n.word_to_num(value)
        except ValueError:
            return None

def add_weather_type_column(data):

    modified_data = []
    
    for line in data:
        parts = line.strip().split(',')
        
        if len(parts) == 5:
            date, city, temperature, humidity, condition = map(str.strip, parts)

            if temperature != "Temperature(C)" or not temperature.isdigit():
                temperature = str(convert_to_number(temperature))
            else:
                temperature_fahrenheit = convert_to_fahrenheit(temperature)
                weather_type = determine_weather_type(temperature_fahrenheit)
                
                modified_line = f"{date}, {city}, {temperature}, {humidity}, {condition}, {weather_type}\n"
                modified_data.append(modified_line)
    
    return modified_data


def handled_data(data):
    missing_value_replaced_rows = []

    for line in data:
        parts = line.strip().split(',')
        if len(parts) == 5:
            date, city, temperature, humidity, condition = map(str.strip, parts)

            if temperature == "":
                temperature = 'null'
            if humidity == "":
                humidity = 'null'
            if condition == "":
                condition = 'null'
            if city == "":
                city = 'null'

            modified_line = f"{date}, {city}, {temperature}, {humidity}, {condition}\n"
            missing_value_replaced_rows.append(modified_line)

    return missing_value_replaced_rows

def main():
    data = read_file()
    
    modified_data = add_weather_type_column(handled_data(data))
    
    result = ''.join(modified_data)
    
    print(result)

if __name__ == '__main__':
    main()
