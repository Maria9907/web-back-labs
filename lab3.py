from flask import Blueprint, redirect, url_for, abort, make_response, request, render_template

lab3 = Blueprint('lab3',__name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')
    return render_template('lab3/lab3.html', name=name, name_color= name_color, age=age)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Maria', max_age=5)
    resp.set_cookie('age', '19')
    resp.set_cookie('name_color', 'magenta')
    return resp

@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'

    age = request.args.get('age')
    if age == '':  
        errors['age'] = 'Заполните поле!'

    sex = request.args.get('sex')

    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)
    

@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')

@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea' :
        price = 80
    else:
        price = 70
    
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/success')
def success():
    price = request.args.get('price', 0)
    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    if color:
        resp = make_response(redirect('/lab3/settings'))
        resp.set_cookie('color', color)
        return resp
    
   
    bg_color = request.args.get('bg_color')
    if bg_color:
        resp = make_response(redirect('/lab3/settings'))
        resp.set_cookie('bg_color', bg_color)
        return resp
    
    
    font_size = request.args.get('font_size')
    if font_size:
        resp = make_response(redirect('/lab3/settings'))
        resp.set_cookie('font_size', font_size)
        return resp
    
   
    font_family = request.args.get('font_family')
    if font_family:
        resp = make_response(redirect('/lab3/settings'))
        resp.set_cookie('font_family', font_family)
        return resp
    
    
    color = request.cookies.get('color')
    bg_color = request.cookies.get('bg_color')
    font_size = request.cookies.get('font_size')
    font_family = request.cookies.get('font_family')
    
    resp = make_response(render_template('lab3/settings.html', 
                                       color=color, 
                                       bg_color=bg_color, 
                                       font_size=font_size, 
                                       font_family=font_family))
    return resp

@lab3.route('/lab3/settings/clear')
def clear_settings():
    resp = make_response(redirect('/lab3/settings'))
    cookies_to_clear = ['color', 'bg_color', 'font_size', 'font_family']
    for cookie_name in cookies_to_clear:
        resp.set_cookie(cookie_name, '', expires=0)
    return resp



@lab3.route('/lab3/form2')
def form2():
    
    last_name = request.args.get('last_name', '')
    first_name = request.args.get('first_name', '')
    middle_name = request.args.get('middle_name', '')
    age = request.args.get('age', '')
    departure = request.args.get('departure', '')
    destination = request.args.get('destination', '')
    date = request.args.get('date', '')
    shelf = request.args.get('shelf', '')
    bedding = request.args.get('bedding', '')
    luggage = request.args.get('luggage', '')
    insurance = request.args.get('insurance', '')
    
   
    errors = {
        'last_name': request.args.get('error_last_name', ''),
        'first_name': request.args.get('error_first_name', ''),
        'middle_name': request.args.get('error_middle_name', ''),
        'age': request.args.get('error_age', ''),
        'departure': request.args.get('error_departure', ''),
        'destination': request.args.get('error_destination', ''),
        'date': request.args.get('error_date', ''),
        'shelf': request.args.get('error_shelf', '')
    }
    
    return render_template('lab3/form2.html',
                         last_name=last_name, first_name=first_name, middle_name=middle_name,
                         age=age, departure=departure, destination=destination, date=date,
                         shelf=shelf, bedding=bedding, luggage=luggage, insurance=insurance,
                         errors=errors)




@lab3.route('/lab3/ticket')
def ticket():
    last_name = request.args.get('last_name')
    first_name = request.args.get('first_name')
    middle_name = request.args.get('middle_name')
    age = request.args.get('age')
    departure = request.args.get('departure')
    destination = request.args.get('destination')
    date = request.args.get('date')
    shelf = request.args.get('shelf')
    bedding = request.args.get('bedding')
    luggage = request.args.get('luggage')
    insurance = request.args.get('insurance')
    
    age_int = int(age)
    if age_int < 18:
        ticket_type = "Детский билет"
        price = 700
    else:
        ticket_type = "Взрослый билет" 
        price = 1000
    
    
    if shelf in ['lower', 'lower-side']:
        price += 100
    
    if bedding == 'on':
        price += 75
    
    if luggage == 'on':
        price += 250
    
    if insurance == 'on':
        price += 150
    
    
    return render_template('lab3/ticket.html',
                         last_name=last_name, first_name=first_name, middle_name=middle_name,
                         age=age, departure=departure, destination=destination, date=date,
                         shelf=shelf, bedding=bedding, luggage=luggage, insurance=insurance,
                         ticket_type=ticket_type, price=price)





products = [
    {"name": "iPhone 15", "price": 89990, "brand": "Apple", "color": "черный", "storage": "128GB"},
    {"name": "Samsung Galaxy S24", "price": 74990, "brand": "Samsung", "color": "белый", "storage": "256GB"},
    {"name": "Xiaomi Redmi Note 13", "price": 24990, "brand": "Xiaomi", "color": "синий", "storage": "128GB"},
    {"name": "Google Pixel 8", "price": 69990, "brand": "Google", "color": "серый", "storage": "128GB"},
    {"name": "OnePlus 12", "price": 59990, "brand": "OnePlus", "color": "зеленый", "storage": "256GB"},
    {"name": "Realme 11 Pro", "price": 29990, "brand": "Realme", "color": "золотой", "storage": "128GB"},
    {"name": "Honor Magic 6", "price": 54990, "brand": "Honor", "color": "фиолетовый", "storage": "256GB"},
    {"name": "Vivo X100", "price": 64990, "brand": "Vivo", "color": "черный", "storage": "256GB"},
    {"name": "Oppo Find X7", "price": 79990, "brand": "Oppo", "color": "белый", "storage": "512GB"},
    {"name": "iPhone 14", "price": 69990, "brand": "Apple", "color": "красный", "storage": "128GB"},
    {"name": "Samsung Galaxy A54", "price": 34990, "brand": "Samsung", "color": "фиолетовый", "storage": "128GB"},
    {"name": "Xiaomi Poco X6", "price": 27990, "brand": "Xiaomi", "color": "желтый", "storage": "256GB"},
    {"name": "Google Pixel 7a", "price": 44990, "brand": "Google", "color": "голубой", "storage": "128GB"},
    {"name": "Nothing Phone 2", "price": 49990, "brand": "Nothing", "color": "белый", "storage": "256GB"},
    {"name": "Asus ROG Phone 8", "price": 89990, "brand": "Asus", "color": "черный", "storage": "512GB"},
    {"name": "Sony Xperia 5 V", "price": 79990, "brand": "Sony", "color": "синий", "storage": "256GB"},
    {"name": "Motorola Edge 40", "price": 39990, "brand": "Motorola", "color": "зеленый", "storage": "256GB"},
    {"name": "Nokia G42", "price": 19990, "brand": "Nokia", "color": "фиолетовый", "storage": "128GB"},
    {"name": "Tecno Camon 20", "price": 15990, "brand": "Tecno", "color": "синий", "storage": "128GB"},
    {"name": "Infinix Note 30", "price": 17990, "brand": "Infinix", "color": "золотой", "storage": "256GB"},
    {"name": "iPhone 15 Pro", "price": 119990, "brand": "Apple", "color": "титан", "storage": "256GB"},
    {"name": "Samsung Galaxy Z Flip5", "price": 99990, "brand": "Samsung", "color": "фиолетовый", "storage": "256GB"},
    {"name": "Xiaomi 13T", "price": 49990, "brand": "Xiaomi", "color": "черный", "storage": "256GB"}
]

@lab3.route('/lab3/search')
def search():
    min_price = request.args.get('min_price', '')
    max_price = request.args.get('max_price', '')
    reset = request.args.get('reset')
    
    
    if reset:
        resp = make_response(redirect('/lab3/search'))
        resp.delete_cookie('min_price')
        resp.delete_cookie('max_price')
        return resp
    
   
    if not min_price:
        min_price = request.cookies.get('min_price', '')
    if not max_price:
        max_price = request.cookies.get('max_price', '')
    
   
    all_prices = [product['price'] for product in products]
    global_min_price = min(all_prices)
    global_max_price = max(all_prices)
    
    
    filtered_products = products
    
    if min_price or max_price:
        
        min_val = float(min_price) if min_price else global_min_price
        max_val = float(max_price) if max_price else global_max_price
        
        
        if min_val > max_val:
            min_val, max_val = max_val, min_val  
            min_price, max_price = str(min_val), str(max_val)  
        filtered_products = [
            product for product in products
            if min_val <= product['price'] <= max_val
        ]
        
        
        resp = make_response(render_template('lab3/search.html',
                                            products=filtered_products,
                                            min_price=min_price,
                                            max_price=max_price,
                                            global_min_price=global_min_price,
                                            global_max_price=global_max_price))
        if min_price:
            resp.set_cookie('min_price', min_price)
        if max_price:
            resp.set_cookie('max_price', max_price)
        return resp
        
        
    return render_template('lab3/search.html',
                         products=filtered_products,
                         min_price=min_price,
                         max_price=max_price,
                         global_min_price=global_min_price,
                         global_max_price=global_max_price)