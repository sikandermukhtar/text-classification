import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Automatically update to the async driver if not already specified
if DATABASE_URL is None:
    DATABASE_URL = "sqlite+aiosqlite:///./development_for_aiml.db"
    engine = create_async_engine(DATABASE_URL)
else:
    # Ensure the driver is postgresql+psycopg
    if "postgresql" in DATABASE_URL and "+psycopg" not in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://")
    engine = create_async_engine(DATABASE_URL)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    autoflush=False, 
    expire_on_commit=False
)
