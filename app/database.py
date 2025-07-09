from sqlalchemy import create_engine , text
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from urllib.parse import quote_plus

DB_USERNAME = "memory.storage"
DB_PASSWORD = quote_plus("Arushi100@")
DB_HOST = "localhost"        
DB_PORT = 3306
DB_NAME = "memory"

SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_connection():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("fetched your happy moments")
    except Exception as e:
        print("your moments are lost", e)
