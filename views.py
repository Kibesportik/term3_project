from config import app, templates
from db import get_db, Tour , User
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Request, Depends, Form
from sqlalchemy.orm import Session

@app.get('/',response_class=HTMLResponse)
def index(request:Request):
    return templates.TemplateResponse('index.html',{'request': request})

@app.post('/register')
def register(
        username: str = Form(),
        email: str = Form(),
        password: str = Form(),
        confirm_psw: str = Form(),
        db : Session = Depends(get_db)):
    print(username,email,password,confirm_psw)
    return RedirectResponse('/',status_code=302)