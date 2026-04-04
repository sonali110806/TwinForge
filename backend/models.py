from sqlalchemy import create_engine, Column, Integer, String, Float, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://twin:twin@localhost:5432/digitwin")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


class Twin(Base):
    __tablename__ = "twins"

    id     = Column(Integer, primary_key=True, index=True)
    name   = Column(String,  nullable=False)
    status = Column(String,  default="healthy")
    cpu    = Column(Float,   default=0.0)
    memory = Column(Float,   default=0.0)
    config = Column(JSON,    default=dict)


def init_db():
    Base.metadata.create_all(bind=engine)
