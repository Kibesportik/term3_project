from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


DATABASE_URI = 'sqlite:///app.db'


engine = create_engine(DATABASE_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    is_admin = Column(Boolean, nullable=False)


class Tour(Base):
    __tablename__ = 'tour'
    id = Column(Integer, primary_key=True)
    tour_name = Column(String(20), unique=True, nullable=False)
    city = Column(String(20), nullable=False)
    is_vacant = Column(Boolean, nullable=False)
    quantity = Column(Integer, nullable=False)
    tour_date = Column(String(30), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Integer, nullable=False)
