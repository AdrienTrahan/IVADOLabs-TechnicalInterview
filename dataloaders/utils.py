from unidecode import unidecode
import re

def formatCity(cityName):
    cityName = unidecode(cityName).lower()
    cityName = re.sub(r'[^a-zA-Z,]', '', cityName)
    cityName = cityName.replace('city', '')
    cityNames = cityName.split(",");
    return cityNames