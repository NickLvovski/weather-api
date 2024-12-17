"""Creating database for weather requests"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Создание директории для базы данных, если ее нет
os.makedirs("data", exist_ok=True)

SQLALCHEMY_DATABASE_URL = "sqlite:///data/weather.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
