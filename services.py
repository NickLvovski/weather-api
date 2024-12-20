"""GET methods for API"""
from statistics import mean
import requests
from fastapi import HTTPException
from credentials import WEATHERSTACK_API_KEY

WEATHERSTACK_BASE_URL = "http://api.weatherstack.com/"

def get_weather(city:str) -> dict:
    """Получение текущего прогноза погоды"""
    url = f"{WEATHERSTACK_BASE_URL}/current"
    params = {"access_key": WEATHERSTACK_API_KEY, "query": city}
    responce = requests.get(url, params=params)
    if responce.status_code != 200:
        raise HTTPException(status_code=404, detail="Weather data not found")
    
    weather_data = responce.json()
    return {
        "city": city,
        "temperature": weather_data["current"]["temperature"],
        "feelslike": weather_data["current"]["feelslike"],
        "wind_speed": weather_data["current"]["wind_speed"],
        "wind_dir": weather_data["current"]["wind_dir"]
    }

