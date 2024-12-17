"""Main module"""
from fastapi import FastAPI, HTTPException
from services import get_weather
from models import WeatherRequest, Base
from database import SessionLocal, engine
from sqlalchemy.orm import Session

app = FastAPI(title="Weather API", version="1.0.0")

#Creating database
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/weather", summary="Get weather forecast")
def weather(city: str):
    """
    Получает текущий прогноз погоды и сохраняет его в базу данных.
    """
    try:
        weather_data = get_weather(city)

        db = SessionLocal()
        weather_request = WeatherRequest(
            city=city,
            temperature=weather_data["temperature"],
            feelslike=weather_data["feelslike"],
            wind_speed=weather_data["wind_speed"],
            wind_dir=weather_data["wind_dir"]
            )
        db.add(weather_request)
        db.commit()
        db.close()

        return weather_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/weather/history", summary="Get weather history")
def weather_history(city: str):
    """
    Возвращает историю запросов погоды для указанного города.
    """
    db: Session=next(get_db())
    history = db.query(WeatherRequest).filter(WeatherRequest.city == city).all()
    if not history:
        raise HTTPException(status_code=404, detail=f"No history found for city: {city}")
    
    return [
        {
            "id" : record.id,
            "city": record.city,
            "temperature": record.temperature,
            "feelslike": record.feelslike,
            "wind_speed": record.wind_speed,
            "wind_dir": record.wind_dir,
            "created_at": record.created_at
        }
        for record in history
    ]
