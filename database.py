import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from dotenv import load_dotenv

load_dotenv()


PASSWORD = os.getenv("POSTGRES_PASSWORD")  
USER = os.getenv("USER") 
HOST = os.getenv("HOST") 
PORT = os.getenv("PORT") 
DB_NAME = os.getenv("DB_NAME") 

# 2. Ulanish URL-manzilini yaratish
DATABASE_URL = f"postgresql://postgres:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"



engine = create_engine(
    DATABASE_URL  
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
