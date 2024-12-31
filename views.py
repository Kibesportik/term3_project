from config import app, templates
from db import get_db, Tour, User, Order
from fastapi.responses import HTMLResponse, JSONResponse
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
    if request.session['is_login']:
        is_admin = db.query(User).get(user_id).is_admin
        ordered_tours = db.query(Order).filter_by(user_id=user_id)
        tour_list = []
        order_amount_list = []
        city_list = []
        date_list = []
        user_order_list = []
        id_list = []
        for i in ordered_tours:
            tour_list.append(i.tour_id)
            order_amount_list.append(i.order_amount)
            id_list.append(i.id)
        for i in tour_list:
            list_example = db.query(Tour).get(i)
            city_list.append(list_example.city)
            date_list.append(list_example.tour_date)
        a = 0
        for i in range(len(tour_list)):
            i = {'id': id_list[a], 'city': city_list[a], 'tour_date': date_list[a], 'amount': order_amount_list[a]}
            user_order_list.append(i)
            a += 1
        return templates.TemplateResponse('profile.html', {'request': request,
                                                           'current_user': request.session['username'],
                                                           'user_id': request.session['user_id'], 'is_admin': is_admin,
                                                           'user_order_list': user_order_list})
    return templates.TemplateResponse('error.html', {'request': request})


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
    if request.session['is_login'] and request.session['is_admin']:
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
    return templates.TemplateResponse('error.html', {'request': request})


@app.post('/tour_order/{tour_id}')
def tour_order(request: Request,
               tour_id: int,
               order_amount: int = Form(),
               db: Session = Depends(get_db)):
    if request.session['is_login']:
        if 0 <= order_amount <= 50:
            new_ordered_tour = db.query(Tour).get(tour_id)
            if new_ordered_tour.quantity >= 0 and new_ordered_tour.quantity-order_amount >= 0:
                user_id = request.session['user_id']
                ordered_tours = db.query(Order).filter_by(user_id=user_id)
                orders_amount_list = []
                for i in ordered_tours:
                    if i.order_amount == tour_id:
                        orders_amount_list.append(i.order_amount)
                new_ordered_tour.quantity = new_ordered_tour.quantity - order_amount
                db.commit()
                db.refresh(new_ordered_tour)
                current_amount = new_ordered_tour.quantity
                order = Order(user_id=user_id, tour_id=tour_id, order_amount=order_amount)
                db.add(order)
                db.commit()
            else:
                new_ordered_tour.is_vacant = False
                db.commit()
                return JSONResponse({'error': 'No spaces left'}, status_code=418)
        else:
            return JSONResponse({'error': 'Too many people'}, status_code=418)
        return {'current_amount': current_amount}
    return templates.TemplateResponse('error.html', {'request': request})


@app.post('/change_password')
def change_password(request: Request,
                    db: Session = Depends(get_db),
                    current_psw: str = Form(),
                    new_psw: str = Form()):
    if request.session['is_login']:
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
    return templates.TemplateResponse('error.html', {'request': request})


@app.post('/change_username')
def change_username(request: Request,
                    db: Session = Depends(get_db),
                    new_username: str = Form()):
    if request.session['is_login']:
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
    return templates.TemplateResponse('error.html', {'request': request})


@app.post('/delete_tour')
def delete_tour(request: Request,
                db: Session = Depends(get_db),
                delete_tour_name: str = Form()):
    if request.session['is_login'] and request.session['is_admin']:
        tour_info = db.query(Tour).filter_by(tour_name=delete_tour_name).first()
        tour_orders_list = []
        if tour_info is not None:
            tour_id = tour_info.id
            tour_orders = db.query(Order).filter_by(tour_id=tour_id)
            orders_id_list = []
            orders_tourid_list = []
            orders_final_list = []
            for i in tour_orders:
                orders_id_list.append(i.id)
                orders_tourid_list.append(i.tour_id)
            a = 0
            for i in range(len(orders_id_list)):
                i = {'id': orders_id_list[a], 'tour_id': orders_tourid_list[a]}
                orders_final_list.append(i)
                a += 1
            for i in orders_final_list:
                if i['tour_id'] == tour_id:
                    db.query(Order).filter_by(id=i['id']).delete()
                    db.commit()
            db.query(Tour).filter_by(id=tour_id).delete()
            db.commit()
            if tour_orders is not None:
                for i in tour_orders:
                    tour_orders_list.append(i.tour_id)
        else:
            return JSONResponse({'error': 'Tour doesn`t exist'}, status_code=418)
        return {}
    return templates.TemplateResponse('error.html', {'request': request})


@app.post('/delete_user')
def delete_user(request: Request,
                delete_username: str = Form(),
                db: Session = Depends(get_db)):
    if request.session['is_login'] and request.session['is_admin']:
        user_info = db.query(User).filter_by(username=delete_username).first()
        if user_info is not None:
            user_id = user_info.id
            user_orders = db.query(Order).filter_by(user_id=user_id)
            orders_tourid_list = []
            orders_userid_list = []
            orders_final_list = []
            orders_amount_list = []
            if user_orders is not None:
                for i in user_orders:
                    orders_userid_list.append(i.user_id)
                    orders_amount_list.append(i.order_amount)
                    orders_tourid_list.append(i.tour_id)
                a = 0
                for i in range(len(orders_userid_list)):
                    i = {'tour_id': orders_tourid_list[a], 'user_id': orders_userid_list[a],
                         'amount': orders_amount_list[a]}
                    orders_final_list.append(i)
                    a += 1
                sum_amount_list = []
                prev_tour = 0
                a = 0
                for i in orders_final_list:
                    if prev_tour != i['tour_id']:
                        sum_amount_list.append({'tour_id': i['tour_id'], 'amount': i['amount']})
                    else:
                        sum_amount_list[a]['amount'] += i['amount']
                        a += 1
                    prev_tour = i['tour_id']
                for i in sum_amount_list:
                    ordered_tour = db.query(Tour).get(i['tour_id'])
                    ordered_tour.quantity = ordered_tour.quantity + i['amount']
                    db.commit()
                    db.refresh(ordered_tour)
                db.query(User).filter_by(username=delete_username).delete()
                db.commit()
            else:
                return JSONResponse({'error': 'Tour doesn`t exist'}, status_code=418)
        else:
            return JSONResponse({'error': 'Tour doesn`t exist'}, status_code=418)
        return {}
    return templates.TemplateResponse('error.html', {'request': request})


@app.post('/add_admin')
def add_admin(
        request: Request,
        username: str = Form(),
        email: str = Form(),
        password: str = Form(),
        confirm_psw: str = Form(),
        db: Session = Depends(get_db)):
    if request.session['is_login'] and request.session['is_admin']:
        reg_email = db.query(User).filter_by(email=email).first()
        reg_username = db.query(User).filter_by(username=username).first()
        if reg_email is None and reg_username is None:
            if 4 <= len(username) <= 25:
                if password == confirm_psw and 4 <= len(password) <= 20:
                    user = User(username=username, email=email, password=password, is_admin=True)
                    db.add(user)
                    db.commit()
                else:
                    return JSONResponse({'error': 'Passwords don`t match or incorrect length'}, status_code=418)
            else:
                return JSONResponse({'error': 'Username is too short'}, status_code=418)
        else:
            return JSONResponse({'error': 'User already exists'}, status_code=418)
        return {}
    return templates.TemplateResponse('error.html', {'request': request})


@app.post('/search')
def search(db: Session = Depends(get_db),
           search_word: str = Form()):
    tours = db.query(Tour).all()
    tour_id_list = []
    if search_word != '':
        for i in tours:
            if not search_word.lower() in i.city.lower():
                tour_id_list.append(i.id)
        return {'tour_id_list': tour_id_list}
    elif len(search_word) >= 2 and len(tour_id_list) == 0:
        for i in tours:
            tour_id_list.append(i.id)
        return {'tour_id_list': tour_id_list}
    elif search_word == '':
        for i in tours:
            tour_id_list.append(i.id)
        return JSONResponse({'tour_id_list': tour_id_list}, status_code=418)


@app.get('/logout', response_class=HTMLResponse)
def logout(request: Request, db: Session = Depends(get_db)):
    request.session['user_id'] = None
    request.session['username'] = ''
    request.session['is_login'] = False
    request.session['is_admin'] = False
    tour_list = db.query(Tour).all()
    tour_id_list = []
    final_tour_list = []
    for tour_id in tour_list:
        tour_id_list.append(tour_id.id)
    for i in tour_id_list:
        tour_example = db.query(Tour).get(i)
        final_tour_list.append(tour_example)
    return templates.TemplateResponse('index.html', {'request': request, 'current_user': request.session['username'],
                                                     'is_login': request.session['is_login'],
                                                     'user_id': request.session['user_id'],
                                                     'is_admin': request.session['is_admin'],
                                                     'tour_list': final_tour_list})