weather_data = []

with open('weather-data.txt', 'r') as file:
    lines = file.readlines()

for line in lines[1:]:
    parts = line.strip().split(',')
    weather_data.append(parts)

consistent_data = {}

date = ''
city = ''
temp_str = ''
humidity_str = ''
condition = ''

for row in weather_data:
    date, city, temp_str, humidity_str, condition = row
    
    if temp_str == "" or humidity_str == "":
        temp_str = 0
        humidity_str = 0

    consistent_data[city] = date, temp_str , humidity_str, condition
    print(consistent_data)

    

        