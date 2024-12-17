"""Models for sqlite database"""
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class WeatherRequest(Base):
    """
    Класс-обертка модели для запросов на прогноз погоды.
    """
    __tablename__ = "weather requests"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    temperature = Column(Float)
    feelslike = Column(Float)
    wind_speed = Column(Float)
    wind_dir = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
