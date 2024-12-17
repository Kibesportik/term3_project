from config import app, templates
from db import get_db, Tour, User
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi import Request, Depends, Form
from sqlalchemy.orm import Session

@app.get('/', response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    tour_list_len = len(db.query(Tour).all())
    tour_list = []
    for tour_id in range(1, tour_list_len + 1):
        tour_example = db.query(Tour).get(tour_id)
        tour_list.append(tour_example)
    return templates.TemplateResponse('index.html', {'request': request, 'current_user': request.session['username'],
                                        'is_login': request.session['is_login'], 'tour_list': tour_list})


@app.post('/register')
def register(
        request: Request,
        username: str = Form(),
        email: str = Form(),
        password: str = Form(),
        confirm_psw: str = Form(),
        db: Session = Depends(get_db)):
    reg_email = db.query(User).filter_by(email=email).first()
    reg_username = db.query(User).filter_by(username=username).first()
    if reg_email is None and reg_username is None:
        if password == confirm_psw and 4 <= len(password) <= 20:
            user = User(username=username, email=email, password=password, is_admin=False)
            db.add(user)
            db.commit()
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            request.session['is_login'] = True
        else:
            return JSONResponse({'error': 'Passwords don`t match or incorrect length'}, status_code=418)
    else:
        return JSONResponse({'error': 'User already exists'}, status_code=418)
    return {'current_user': request.session['username']}


@app.post('/login')
def login(
        request: Request,
        email: str = Form(),
        password: str = Form(),
        db: Session = Depends(get_db)):
    log_info = db.query(User).filter_by(email=email).first()
    if log_info is not None:
        if log_info.password == password:
            request.session['user_id'] = log_info.id
            request.session['username'] = log_info.username
            request.session['is_login'] = True
        else:
            return JSONResponse({'error': 'Passwords don`t match'}, status_code=418)
    else:
        return JSONResponse({'error': 'User don`t exists'}, status_code=418)
    return {'current_user': request.session['username']}


@app.post('/add_tour')
def add_tour(
        request: Request,
        city: str = Form(),
        tour_date: str = Form(),
        tour_quant: int = Form(),
        price: int = Form(),
        description: str = Form(),
        tour_name: str = Form(),
        db: Session = Depends(get_db)):
    tour_info = db.query(Tour).filter_by(tour_name=tour_name).first()
    if tour_info is None:
        if len(description) >= 30:
            if price >= 100:
                tour = Tour(city=city, tour_name=tour_name, quantity=tour_quant, tour_date=tour_date,
                        description=description, price=price, is_vacant=True)
                db.add(tour)
                db.commit()
            else:
                return JSONResponse({'error': 'Price is too low'}, status_code=418)
        else:
            return JSONResponse({'error': 'Tour description is too short'}, status_code=418)
    else:
        return JSONResponse({'error': 'Tour already exists'}, status_code=418)
    return {}

@app.post('/tour_order/{tour_id}')
def tour_order(request: Request,
               tour_id: int,
               order_amount: int = Form(),
               db: Session = Depends(get_db)):
    if 0 <= order_amount <= 100 :
        ordered_tour = db.query(Tour).get(tour_id)
        ordered_tour.quantity = ordered_tour.quantity - order_amount
        db.commit()
        db.refresh(ordered_tour)
    return {}
