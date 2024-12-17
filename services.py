import requests
from fastapi import HTTPException

#указан на оф. сайте, не конфиденциальная информация
GISMETEO_API_KEY = "56b30cb255.3443075" 
GISMETEO_BASE_URL = "https://api.gismeteo.net/v2"

def get_location_id(city: str) -> int:
    """Получение ID города."""
    url = f"{GISMETEO_BASE_URL}/location/search"
    headers = {"X-Gismeteo-Token": GISMETEO_API_KEY}
    params = {"query": city}

    responce = requests.get(url, headers=headers, params=params)
    if responce.status_code != 200:
        raise HTTPException(status_code=404, detail="City not found :(")
    return responce.json()["responce"][0]["id"]

def get_weather(city:str) -> dict:
    """Получение текущего прогноза погоды"""
    location_id = get_location_id(city)
    url = f"{GISMETEO_BASE_URL}/weather/current/{location_id}/"
    headers = {"X-Gismeteo-Token": GISMETEO_API_KEY}
    responce = requests.get(url, headers=headers)
    if responce.status_code != 200:
        raise HTTPException(status_code=404, detail="Weather data not found")
    
    weather_data = responce.json["responce"]
    return {
        "city": city,
        "temperature": weather_data["temperature"]["air"]["C"],
        "condition": weather_data["description"]["full"]
    }
