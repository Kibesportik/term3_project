from config import app, templates
from db import get_db, Tour , User
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request, Depends, Form
from sqlalchemy.orm import Session

def login_user(username,db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=username).first()
    if user is None:
        return RedirectResponse(url='/login', status_code=302)

@app.get('/',response_class=HTMLResponse)
def index(request:Request, db: Session = Depends(get_db), username: str = Form()):
    login_user(username)
    return templates.TemplateResponse('index.html',{'request': request})