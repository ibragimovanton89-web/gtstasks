import requests

def сelsius_degree():
    url = "https://api.openweathermap.org/data/2.5/weather?q=Surgut&appid=3a8d5df94cfa9dbd8086c13a71a75838"
    data = requests.get(url).json()
    tempK = data['main']['temp']
    tempC = round(tempK - 273.15, 1)
    return tempC

if __name__ == '__main__':
    сelsius_degree()





