"""Main module"""
import base64
from typing import Annotated
from fastapi import FastAPI, HTTPException, Response, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from prometheus_fastapi_instrumentator import Instrumentator
from services import get_weather
from models import WeatherRequest, Administrator, Base
from database import SessionLocal, engine
from init import init_administrator

app = FastAPI(title="Weather API", version="1.0.1")
security = HTTPBasic()

#Настройка инструментатора для сбора метрик FastAPI
Instrumentator = Instrumentator()
Instrumentator.instrument(app)
Instrumentator.expose(app)

#Creating database
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Administrator initialization
def admin_initialization():
    db = SessionLocal()
    db.add(init_administrator())
    db.commit()
    db.close()
admin_initialization()

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

@app.delete("/weather/history", summary="Remove weather history by id")
def remove_weather_history(
    id:int, 
    credentials:Annotated[HTTPBasicCredentials, Depends(security)]
    ):
    """
    Удаляет запрос из базы данных по id.
    """
    def remove_weather_history(
    id:int, 
    credentials:Annotated[HTTPBasicCredentials, Depends(security)]
    ):
    """
    Удаляет запрос из базы данных по id.
    """
    db: Session=next(get_db())
    # Проверяем, является ли пользователь администратором
    admin = db.query(Administrator).filter(
        Administrator.username == credentials.username
        ).first()
    if not admin:
        raise HTTPException(status_code=401, detail="Administrator not found")
    
    stored_password = base64.b64decode(admin.password).decode('ascii')
    if stored_password != credentials.password:
        raise HTTPException(status_code=401, detail="Wrong password")

    history = db.query(WeatherRequest).filter(WeatherRequest.id == id)
    if not history:
        raise HTTPException(status_code = 404, detail=f"No data for id: {id}")
    db.query(WeatherRequest).filter(WeatherRequest.id == id).delete()
    db.commit()

    return Response(status_code=200)
