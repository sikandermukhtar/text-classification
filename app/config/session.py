import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

load_dotenv()

DATABASE_URL = os.getenv('NEON_DATABSE_URL')

if DATABASE_URL is None:
    DATABASE_URL = "sqlite+pysqlite:///./development_for_aiml"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
