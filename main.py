# uvicorn main:app --reload
from db import engine, Base
from views import *
from config import app

Base.metadata.create_all(engine)