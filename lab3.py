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

    
    if errors:
        return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)
    else:
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