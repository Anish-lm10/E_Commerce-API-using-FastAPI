from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine(
    "postgresql://postgres:anish123@localhost:5432/e_commerce", echo=True
)

SessionLocal = sessionmaker()

Base = declarative_base()
