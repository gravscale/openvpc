from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from .settings import get_settings

settings = get_settings()


url = URL.create(
    drivername="mysql+aiomysql",
    username=settings.MYSQL_USERNAME,
    password=settings.MYSQL_PASSWORD,
    host=settings.MYSQL_HOST,
    port=settings.MYSQL_PORT,
    database=settings.MYSQL_DATABASE,
)

engine = create_async_engine(url, echo=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()
