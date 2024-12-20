# uvicorn main:app --reload
# git rm -r --cached <path_to_file>
from db import engine, Base
from views import *
from config import app

Base.metadata.create_all(engine)
