from flask import Blueprint, redirect, url_for, abort, session, make_response, request, render_template

lab4 = Blueprint('lab4',__name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')

@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')

    x1 = int(x1)
    x2 = int(x2)
    if x2 == 0:
        return render_template('lab4/div.html', error='На ноль делить нельзя!')
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')

@lab4.route('/lab4/sum', methods = ['POST'])
def sum():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '':
        x1 = 0
    else:
        x1 = int(x1) 
    if x2 == '':
        x2 = 0
    else:
        x2 = int(x2)

    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('lab4/mul-form.html')

@lab4.route('/lab4/mul', methods = ['POST'])
def mul():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '':
        x1 = 1
    else:
        x1 = int(x1) 
    if x2 == '':
        x2 = 1
    else:
        x2 = int(x2)

    result = x1 * x2
    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)



@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')

@lab4.route('/lab4/sub', methods = ['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/exp-form')
def exp_form():
    return render_template('lab4/exp-form.html')

@lab4.route('/lab4/exp', methods = ['POST'])
def exp():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/exp.html', error='Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    if x1 == 0 and x2 == 0 :
        return render_template('lab4/exp.html', error='Два поля не могут быть 0!')
    result = x1 ** x2
    return render_template('lab4/exp.html', x1=x1, x2=x2, result=result)

tree_count = 0

@lab4.route('/lab4/tree', methods = ['GET','POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)
    
    operation = request.form.get('operation')

    if operation == 'cut':
        if tree_count > 0:
            tree_count -= 1
    elif operation == 'plant':
        if tree_count < 10:
            tree_count += 1

    return redirect('/lab4/tree')


users = [
    {'login': 'alex1287', 'password': '123', 'name': 'Алексей', 'gender': 'м'},
    {'login': 'maria23ok', 'password': '890', 'name': 'Мария', 'gender': 'ж'},
    {'login': 'temayhyy', 'password': 'zxc', 'name': 'Артем', 'gender': 'м'},
    {'login': 'Машaaat6t', 'password': 'qwerty', 'name': 'Мария', 'gender': 'ж'},
]

@lab4.route('/lab4/login', methods = ['GET','POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            for user in users:
                if user['login'] == session['login']:
                    name = user['name']
                    gender = user['gender']
                    break
        else:
            authorized = False
            name = ''
            gender = ''
        return render_template("lab4/login.html", authorized=authorized, name=name, gender=gender)
    
    login = request.form.get('login')
    password = request.form.get('password')


    if not login:
        error = 'Не введён логин'
        return render_template('/lab4/login.html', error=error, authorized=False, login=login)
    
    if not password:
        error = 'Не введён пароль'
        return render_template('/lab4/login.html', error=error, authorized=False, login=login)



    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            return redirect('/lab4/login')
        
    error = 'Неверные логин и/или пароль'
    return render_template('/lab4/login.html', error=error, authorized=False, login=login)

@lab4.route('/lab4/logout', methods = ['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/fridge', methods = ['GET','POST'])
def fridge():
    if request.method == 'GET':
        return render_template('lab4/fridge.html')
    
    error = None
    message = None
    snowflakes = 0 

    temperature_str = request.form.get('temperature')

    if temperature_str == '':
        error = 'Температура не задана'
        return render_template('lab4/fridge.html', error=error)
    
    temperature = int(temperature_str)

    if temperature < -12:
            error = 'Не удалось установить температуру — слишком низкое значение'
            return render_template('lab4/fridge.html', error=error,  temperature=temperature)
    elif temperature > -1:
        error = 'Не удалось установить температуру — слишком высокое значение'
        return render_template('lab4/fridge.html', error=error,  temperature=temperature)
    elif -12 <= temperature <= -9:
        snowflakes = 3
        message = f'Установлена температура: {temperature}°C'
    elif -8 <= temperature <= -5:
        snowflakes = 2
        message = f'Установлена температура: {temperature}°C'
    elif -4 <= temperature <= -1:
        snowflakes = 1
        message = f'Установлена температура: {temperature}°C'
    else:
        snowflakes = 0
        message = f'Установлена температура: {temperature}°C'

    return render_template('lab4/fridge.html', 
                             message=message, 
                             snowflakes=snowflakes,
                             temperature=temperature)





@lab4.route('/lab4/grain', methods=['GET', 'POST'])
def grain():
    if request.method == 'GET':
        return render_template('lab4/grain.html')
    
    grain = request.form.get('grain')  
    weight_str = request.form.get('weight')
    
    
    prices = {
        'barley': 12000,  # ячмень
        'oats': 8500,     # овёс
        'wheat': 9000,    # пшеница
        'rye': 15000      # рожь
    }
    
    grain_names = {
        'barley': 'ячмень',
        'oats': 'овёс', 
        'wheat': 'пшеница',
        'rye': 'рожь'
    }
    
    error = None
    message = None
    discount_info = None

    if not grain:
        error = 'Ошибка: вы забыли указать зерно'
    elif not weight_str or weight_str.strip() == '':
        error = 'Ошибка: не указан вес'
    else:
        weight = int(weight_str)
        if weight <= 0:
            error = 'Ошибка: вес должен быть положительным числом'
        elif weight > 100:
            error = 'Такого объёма сейчас нет в наличии'
        elif weight > 10:
            # Расчет с скидкой 10%
            base_price = prices[grain]
            total = weight * base_price
            discount = total * 0.1
            final_price = total - discount
            discount_info = f'Применена скидка 10% за большой объём. Размер скидки: {discount:.0f} руб.'
            message = f'Заказ успешно сформирован. Вы заказали {grain_names[grain]}. Вес: {weight} т. Сумма к оплате: {final_price:.0f} руб.'
        else:
            base_price = prices[grain]
            total = weight * base_price
            message = f'Заказ успешно сформирован. Вы заказали {grain_names[grain]}. Вес: {weight} т. Сумма к оплате: {total:.0f} руб.'
        
    return render_template('lab4/grain.html', 
                         error=error, 
                         message=message, 
                         discount_info=discount_info,
                         selected_grain=grain, 
                         weight=weight_str if weight_str else ''
                        )