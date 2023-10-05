import requests
from passwords.weather_api_key import API_KEY



def get_city_temperature(city: str) -> float:
    """This Function Get City Temperature From Api Openweatermap

    Args:
        city (str): City Name To Check Temperature

    Returns:
        float: Value Of City Temperature
    """
    api_key = API_KEY
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'.format(city,api_key)
    weatherData = requests.get(url).json()
    return weatherData['main']['temp']