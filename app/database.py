import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# .env 파일의 DB 접속정보 불러오기
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# MySQL + PyMySQL 접속주소 생성
DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
)

# SQLAlchemy DB 엔진
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# 이후 API에서 사용할 DB 세션
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)