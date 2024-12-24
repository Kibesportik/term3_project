from config import app, templates
from db import get_db, Tour, User, Order
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi import Request, Depends, Form
from sqlalchemy.orm import Session


@app.get('/', response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    tour_list = db.query(Tour).all()
    tour_id_list = []
    final_tour_list = []
    for tour_id in tour_list:
        tour_id_list.append(tour_id.id)
    for i in tour_id_list:
        tour_example = db.query(Tour).get(i)
        final_tour_list.append(tour_example)
    user_id = request.session['user_id']
    if user_id is not None:
        is_admin = db.query(User).get(user_id)
    else:
        is_admin = False
    return templates.TemplateResponse('index.html', {'request': request, 'current_user': request.session['username'],
                                                     'is_login': request.session['is_login'],
                                                     'user_id': user_id, 'is_admin': is_admin,
                                                     'tour_list': final_tour_list})


@app.get('/profile/{user_id}', response_class=HTMLResponse)
def profile(user_id: int, request: Request, db: Session = Depends(get_db)):
    is_admin = db.query(User).get(user_id).is_admin
    ordered_tours = db.query(Order).filter_by(user_id=user_id)
    tour_list = []
    order_amount_list = []
    city_list = []
    date_list = []
    user_order_list = []
    for i in ordered_tours:
        tour_list.append(i.tour_id)
        order_amount_list.append(i.order_amount)
    for i in tour_list:
        list_example = db.query(Tour).get(i)
        city_list.append(list_example.city)
        date_list.append(list_example.tour_date)
    a = 0
    for i in range(len(tour_list)):
        i = {'city': city_list[a], 'tour_date': date_list[a], 'amount': order_amount_list[a]}
        user_order_list.append(i)
        a += 1
    return templates.TemplateResponse('profile.html', {'request': request, 'current_user': request.session['username'],
                                                       'user_id': request.session['user_id'],
                                                       'is_admin': is_admin,
                                                       'user_order_list': user_order_list})


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
        if 4 <= len(username) <= 25:
            if password == confirm_psw and 4 <= len(password) <= 20:
                user = User(username=username, email=email, password=password, is_admin=False)
                db.add(user)
                db.commit()
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                request.session['is_login'] = True
                request.session['is_admin'] = False
            else:
                return JSONResponse({'error': 'Passwords don`t match or incorrect length'}, status_code=418)
        else:
            return JSONResponse({'error': 'Username is too short'}, status_code=418)
    else:
        return JSONResponse({'error': 'User already exists'}, status_code=418)
    return {'current_user': request.session['username'], 'user_id': request.session['user_id']}


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
            request.session['is_admin'] = log_info.is_admin
        else:
            return JSONResponse({'error': 'Passwords don`t match'}, status_code=418)
    else:
        return JSONResponse({'error': 'User don`t exists'}, status_code=418)
    return {'current_user': request.session['username'], 'user_id': request.session['user_id']}


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
    if 0 <= order_amount <= 50:
        new_ordered_tour = db.query(Tour).get(tour_id)
        if new_ordered_tour.quantity >= 0 and new_ordered_tour.quantity-order_amount >= 0:
            user_id = request.session['user_id']
            ordered_tours = db.query(Order).filter_by(user_id=user_id)
            orders_amount_list = []
            sum_amuont_list = 0
            for i in ordered_tours:
                if i.order_amount == tour_id:
                    orders_amount_list.append(i.order_amount)
            for i in orders_amount_list:
                sum_amuont_list += i
            new_ordered_tour.quantity = new_ordered_tour.quantity - order_amount
            db.commit()
            db.refresh(new_ordered_tour)
            current_amount = new_ordered_tour.quantity
            order = Order(user_id=user_id, tour_id=tour_id, order_amount=order_amount)
            db.add(order)
            db.commit()
        else:
            new_ordered_tour.is_vacant = False
            return JSONResponse({'error': 'No spaces left'}, status_code=418)
    else:
        return JSONResponse({'error': 'Too many people'}, status_code=418)
    return {'current_amount': current_amount}


@app.post('/change_password')
def change_password(request: Request,
                    db: Session = Depends(get_db),
                    current_psw: str = Form(),
                    new_psw: str = Form()):
    user_id = request.session['user_id']
    user_password = db.query(User).get(user_id)
    if current_psw == user_password.password:
        if 4 <= len(new_psw) <= 20:
            user_password.password = new_psw
            db.commit()
            db.refresh(user_password)
        else:
            return JSONResponse({'error': 'New password is too short'}, status_code=418)
    else:
        return JSONResponse({'error': 'Passwords don`t match'}, status_code=418)
    return {}


@app.post('/change_username')
def change_username(request: Request,
                    db: Session = Depends(get_db),
                    new_username: str = Form()):
    user_id = request.session['user_id']
    user_username = db.query(User).get(user_id)
    user_info = db.query(User).filter_by(username=new_username).first()
    if user_info is None:
        if new_username != user_username.username:
            if 4 <= len(new_username) <= 20:
                user_username.username = new_username
                db.commit()
                db.refresh(user_username)
                request.session['username'] = new_username
            else:
                return JSONResponse({'error': 'New username is too short'}, status_code=418)
        else:
            return JSONResponse({'error': 'Same username'}, status_code=418)
    else:
        return JSONResponse({'error': 'Username is already taken'}, status_code=418)
    return {}

@app.post('/delete_tour')
def delete_tour(request: Request,
                db: Session = Depends(get_db),
                delete_tour_name: str = Form()):
    tour_info = db.query(Tour).filter_by(tour_name=delete_tour_name).first()
    tour_orders_list = []
    if tour_info is not None:
        tour_id = tour_info.id
        tour_orders = db.query(Order).filter_by(tour_id=tour_id)
        for i in tour_orders:
            print(i.id)
        db.query(Tour).filter_by(id=tour_id).delete()
        db.commit()
        if tour_orders is not None:
            for i in tour_orders:
                tour_orders_list.append(i.tour_id)
                print(i.tour_id)
    else:
        return JSONResponse({'error': 'Tour doesn`t exist'}, status_code=418)
    return {}


@app.post('/delete_user')
def delete_user(request: Request,
                db: Session = Depends(get_db)):
    return {}


@app.post('/add_admin')
def add_admin(request: Request, db: Session = Depends(get_db)):
    print('dobshe')
    return {}


@app.get('/logout',response_class=HTMLResponse)
def logout(request: Request, db: Session = Depends(get_db)):
    request.session['user_id'] = None
    request.session['username'] = ''
    request.session['is_login'] = False
    request.session['is_admin'] = False
    tour_list_len = len(db.query(Tour).all())
    tour_list = []
    for tour_id in range(1, tour_list_len + 1):
        tour_example = db.query(Tour).get(tour_id)
        tour_list.append(tour_example)
    return templates.TemplateResponse('index.html', {'request': request, 'current_user': request.session['username'],
                                                     'is_login': request.session['is_login'],
                                                     'user_id': request.session['user_id'],
                                                     'is_admin': request.session['is_admin'], 'tour_list': tour_list})
