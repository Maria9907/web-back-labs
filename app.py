from flask import (
    Flask,
    url_for,
    request,
    redirect,
    make_response,
    abort,
    render_template,
)
import datetime

app = Flask(__name__)


@app.errorhandler(400)
def bad_request(err):
    return "Неправильный, некорректный запрос", 400


@app.errorhandler(401)
def unauthorized(err):
    return "Не авторизован", 401


@app.errorhandler(403)
def forbidden(err):
    return "Запрещено (не уполномочен)", 403


@app.errorhandler(405)
def method_not_allowed(err):
    return "Метод не поддерживается", 405


@app.errorhandler(418)
def teapot(err):
    return "Я - чайник", 418


@app.route("/lab1/400")
def route_bad_request():
    abort(400, description="Неправильный, некорректный запрос")


@app.route("/lab1/401")
def route_unauthorized():
    abort(401, description="Не авторизован")


@app.route("/lab1/403")
def route_forbidden():
    abort(403, description="Запрещено (не уполномочен)")


@app.route("/lab1/405")
def route_method_not_allowed():
    abort(405, description="Метод не поддерживается")


@app.route("/lab1/418")
def route_teapot():
    abort(418, description="Я - чайник")


@app.route("/lab1/web")
def web():
    return (
        """<!doctype html>
        <html>
            <body>
                <h1>web-сервер на flask</h1>
                <a href="/lab1/author">author</a>
            <body>
        </html>""",
        200,
        {"X-Server": "sample", "Content-Type": "text/plain; charset=utf-8"},
    )


@app.route("/lab1/author")
def author():
    name = "Матюшкина Мария Дмитриевна"
    group = "ФБИ-32"
    faculty = "ФБ"

    return (
        """<!doctype html>
        <html>
           <body>
                <p>Студент: """
        + name
        + """</p>
                <p>Группа: """
        + group
        + """</p>
                <p>Факультет: """
        + faculty
        + """</p>
                <a href="/lab1/web">web</a>
            <body>
        </html>"""
    )


@app.route("/lab1/image")
def image():
    path = url_for("static", filename="картинка.jpg")
    css_path = url_for("static", filename="lab1.css")
    html_content = f"""<!doctype html> 
<html>
    <head>
        <title>Природа</title>
        <link rel="stylesheet" type="text/css" href="{css_path}">
    </head>
    <body>
        <h1>Природа</h1>
        <img src="{path}">
    </body>
</html>"""
    response = make_response(html_content)
    response.headers["Content-Language"] = "ru-RU"
    response.headers["X-Custom-Header-1"] = "Hello"
    response.headers["X-Custom-Header-2"] = "My lab job"
    return response


count = 0


@app.route("/lab1/clear_counter")
def clear_counter():
    global count
    count = 0
    return redirect("/lab1/counter")


@app.route("/lab1/counter")
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr

    return (
        """
<!doctype html> 
<html>
    <body>
        Сколько раз вы сюда заходили: """
        + str(count)
        + """
        <hr>
        Дата и время: """
        + str(time)
        + """<br>
        запрошенный адрес: """
        + url
        + """<br>
        Ваш IP-адрес: """
        + client_ip
        + """<br>
        <a href="/lab1/clear_counter">Очистить счетчик</a>
    </body>
</html>
"""
    )


@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")


@app.route("/created")
def created():
    return (
        """
<!doctype html> 
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i> что то создано...</i></div>
    </body>
</html>
""",
        201,
    )


@app.route("/")
@app.route("/index")
def index():
    return """
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных:</h1>
         <ul>
            <li>
                <a href="/lab1">Первая лабораторная работа</a>
            </li>
            <li>
                <a href="/lab2">Вторая лабораторная работа</a>
            </li>
        </ul>
            
        <footer>
            <p>Матюшкина Мария Дмитриевна, ФБИ-32, 3 курс, 2025 год</p>
        </footer>
    </body>
</html>
"""


@app.route("/lab1")
def lab1():

    routes = [
        ("/lab1/400", "400 - Неправильный запрос"),
        ("/lab1/401", "401 - Не авторизован"),
        ("/lab1/403", "403 - Запрещено"),
        ("/lab1/404", "404 - Не найдена"),
        ("/lab1/405", "405 - Метод не поддерживается"),
        ("/lab1/418", "418 - Я - чайник"),
        ("/lab1/web", "Web-сервер"),
        ("/lab1/author", "Информация об авторе"),
        ("/lab1/image", "Изображение"),
        ("/lab1/counter", "Счетчик посещений"),
        ("/lab1/info", "Перенаправление на автора"),
        ("/lab1/error", "Генерация ошибки"),
    ]

    routes_html = ""
    for route_url, route_name in routes:
        routes_html += f'<li><a href="{route_url}">{route_name}</a></li>'

    return f"""
<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
    </head>
    <body>
        <p>Flask — фреймворк для создания веб-приложений на языке
            программирования Python, использующий набор инструментов
            Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
            называемых микрофреймворков — минималистичных каркасов
            веб-приложений, сознательно предоставляющих лишь самые ба-
            зовые возможности.</p>
        <a href="/">На главную</a>
        
        <h2>Список роутов</h2>
        <ul>
            {routes_html}
        </ul>
    </body>
</html>
"""


@app.route("/lab1/error")
def cause_error():
    try:
        result = 1 / 0
    except Exception as e:
        print(f"An error occurred: {e}")
        abort(500)
    return "Ошибка"


@app.errorhandler(500)
def internal_server_error(err):
    return "Внутренняя ошибка сервера", 500


access_log = []


@app.errorhandler(404)
def not_found(err):

    client_ip = request.remote_addr
    access_time = datetime.datetime.now()
    requested_url = request.url

    log_entry = (
        f"[{access_time}, пользователь {client_ip}] зашёл на адрес: {requested_url}"
    )
    access_log.append(log_entry)

    css_path = url_for("static", filename="lab1.css")

    log_html = ""
    for entry in access_log:
        log_html += f"<p class='log-entry'>{entry}</p>"

    return (
        f"""<!DOCTYPE html>
<html>
<head>
    <title>Ошибка 404</title>
    <link rel="stylesheet" type="text/css" href="{css_path}">
    
</head>
<body>
    <div class="error-404-container">
        <h1>404</h1>
        <p>Страница, которую вы ищете, не найдена.</p>
        <p><strong>Ваш IP-адрес:</strong> {client_ip}</p>
        <p><strong>Дата доступа:</strong> {access_time}</p>
        <p><a href="/">Вернуться на главную</a></p>
        
        <div class="access-log-container">
            <h2>Журнал посещений:</h2>
            <div class="log-entries">
                {log_html}
            </div>
        </div>
    </div>
</body>
</html>""",
        404,
    )


@app.route("/lab2/a")
def a():
    return "без слэша"


@app.route("/lab2/a/")
def a2():
    return "со слэшем"


flower_list = [
    {'name': 'роза', 'price': 300},
    {'name': 'тюльпан', 'price': 310},
    {'name': 'незабудка', 'price': 320},
    {'name': 'ромашка', 'price': 330},
    {'name': 'георгин', 'price': 300},
    {'name': 'гладиолус', 'price': 310}
]

@app.route("/lab2/flowers/<int:flower_id>")
def flowers(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    flower = flower_list[flower_id]
    return render_template('one_flower.html', flower=flower, flower_id=flower_id)


@app.route("/lab2/add_flower/")
def add_flower_no_name():
    response = make_response("вы не задали имя цветка", 400)
    return response


@app.route("/lab2/add_flower/<name>")
def add_flower(name):
    flower_list.append({'name': name, 'price': 0})
    return render_template('add_flower.html', 
                          name=name, 
                          price=0,
                          count=len(flower_list),
                          flowers=flower_list)

@app.route("/lab2/add_flower", methods=['POST'])
def add_flower_post():
    name = request.form.get('name')
    price = request.form.get('price')
    if name and price:
        flower_list.append({'name': name, 'price': int(price)})
        return redirect(url_for('show_all_flowers'))
    else:
        return render_template('error.html', message="Не указано имя или цена цветка"), 400

@app.route("/lab2/all_flowers")
def show_all_flowers():
    return render_template('all_flowers.html', flowers=flower_list)


@app.route("/lab2/del_flower/<int:flower_id>")
def delete_flower(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    flower_list.pop(flower_id)
    return redirect(url_for('show_all_flowers'))

@app.route("/lab2/example")
def example():
    name, group, course, lab = "Матюшкина Мария", "ФБИ-32", "3 курс", "2"
    fruits = [
        {"name": "яблоки", "price": 100},
        {"name": "груши", "price": 120},
        {"name": "апельсины", "price": 80},
        {"name": "мандарины", "price": 95},
        {"name": "манго", "price": 321},
    ]
    return render_template(
        "example.html", name=name, group=group, course=course, lab=lab, fruits=fruits
    )


@app.route("/lab2/")
def lab2():
    return render_template("lab2.html")


@app.route("/lab2/filters")
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template("filter.html", phrase=phrase)


@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    return render_template('calc.html', a=a, b=b)

@app.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')

@app.route('/lab2/calc/<int:a>')
def calc_single(a):
    return redirect(url_for('calc', a=a, b=1))


books = [
    {"author": "Фёдор Достоевский", "title": "Преступление и наказание", "genre": "Роман", "pages": 671},
    {"author": "Лев Толстой", "title": "Война и мир", "genre": "Роман-эпопея", "pages": 1225},
    {"author": "Антон Чехов", "title": "Рассказы", "genre": "Рассказ", "pages": 350},
    {"author": "Михаил Булгаков", "title": "Мастер и Маргарита", "genre": "Роман", "pages": 480},
    {"author": "Александр Пушкин", "title": "Евгений Онегин", "genre": "Роман в стихах", "pages": 240},
    {"author": "Николай Гоголь", "title": "Мёртвые души", "genre": "Поэма", "pages": 352},
    {"author": "Иван Тургенев", "title": "Отцы и дети", "genre": "Роман", "pages": 288},
    {"author": "Александр Солженицын", "title": "Архипелаг ГУЛАГ", "genre": "Художественно-историческое произведение", "pages": 1424},
    {"author": "Владимир Набоков", "title": "Лолита", "genre": "Роман", "pages": 336},
    {"author": "Михаил Лермонтов", "title": "Герой нашего времени", "genre": "Роман", "pages": 224},
    {"author": "Илья Ильф, Евгений Петров", "title": "Двенадцать стульев", "genre": "Роман", "pages": 416},
    {"author": "Борис Пастернак", "title": "Доктор Живаго", "genre": "Роман", "pages": 592}
]
@app.route('/lab2/books')
def show_books():
    return render_template('books.html', books=books)



cat_breeds = [
    {
        "id": 1,
        "breed": "Британская короткошёрстная",
        "description": "Британская короткошёрстная кошка - порода кошек, зародившаяся в Великобритании в XIX веке. Иногда называется «плюшевой» или «картофельной» кошкой за мягкую, плотно прилегающую шерсть и крепкое телосложение. Характер спокойный, независимый.",
        "image": "британец.jpg"
    },
    {
        "id": 2,
        "breed": "Мейн-кун",
        "description": "Мейн-кун - крупная порода домашних кошек, произошедшая от кошек штата Мэн в Северной Америке. Это одна из старейших естественных пород Северной Америки. Отличаются кисточками на ушах, длинным пушистым хвостом и дружелюбным характером.",
        "image": "мейк-ун.jpg"  
    },
    {
        "id": 3,
        "breed": "Сиамская кошка",
        "description": "Сиамская кошка - одна из известных пород кошек родом из Таиланда (ранее Сиам). Отличается элегантным телом, клиновидной головой, ярко-голубыми глазами и колор-пойнтовым окрасом. Очень разговорчивая и привязчивая порода.",
        "image": "сиамская.jpg"  
    },
    {
        "id": 4,
        "breed": "Персидская кошка",
        "description": "Персидская кошка - длинношёрстная порода кошек, характеризующаяся круглой мордой и коротким носом. Имеет очень густую и пушистую шерсть, требующую ежедневного ухода. Характер спокойный и флегматичный.",
        "image": "персидская.jpg" 
    },
    {
        "id": 5,
        "breed": "Сфинкс",
        "description": "Канадский сфинкс - бесшёрстная порода кошек, выведенная в 1960-х годах в Канаде. Несмотря на отсутствие шерсти, тело покрыто тонким пушком. Требуют особого ухода за кожей и защиты от солнца. Температура тела выше, чем у других кошек.",
        "image": "свинкс.jpg"  
    },
    {
        "id": 6,
        "breed": "Шотландская вислоухая",
        "description": "Шотландская вислоухая кошка - порода с характерными загнутыми вперёд и вниз ушами. Мутация, вызывающая вислоухость, может также влиять на развитие хрящей в других частях тела. Имеют спокойный и дружелюбный характер.",
        "image": "вислоухая.jpg" 
    },
    {
        "id": 7,
        "breed": "Русская голубая",
        "description": "Русская голубая кошка - порода домашней кошки, признанная международными фелинологическими организациями. Отличается короткой плюшевой шерстью голубого цвета с серебристым отливом, зелёными глазами и изящным телосложением.",
        "image": "русская.jpg"  
    },
    {
        "id": 8,
        "breed": "Бенгальская кошка",
        "description": "Бенгальская кошка - гибрид домашней кошки и дикого азиатского леопардового кота. Имеет характерный леопардовый окрас и дикую внешность, но домашний характер. Очень активные, умные и любят воду.",
        "image": "бенгальская.jpg"  
    },
    {
        "id": 9,
        "breed": "Норвежская лесная кошка",
        "description": "Норвежская лесная кошка - порода домашних полудлинношёрстных кошек, произошедшая от диких лесных кошек Норвегии. Имеет густую водонепроницаемую шерсть, кисточки на ушах и пушистый хвост. Отличные охотники.",
        "image": "норвежская.jpg"  
    },
    {
        "id": 10,
        "breed": "Абиссинская кошка",
        "description": "Абиссинская кошка - одна из древнейших пород кошек. Отличается характерным тикированным окрасом, при котором каждый волосок имеет несколько полос разного цвета. Стройные, грациозные, очень активные и любознательные.",
        "image": "абиссинская2.jpg" 
    },
    {
        "id": 11,
        "breed": "Рэгдолл",
        "description": "Рэгдолл - порода полудлинношёрстных кошек. Название породы переводится как 'тряпичная кукла', что отражает их характерную особенность - расслаблять мышцы тела, когда их берут на руки. Очень спокойные и ласковые.",
        "image": "рэгдолл.jpg" 
    },
    {
        "id": 12,
        "breed": "Ориентальная кошка",
        "description": "Ориентальная кошка - порода, родственная сиамской, но имеющая сплошной окрас без пойнтов. Отличается большими ушами, стройным телом и клиновидной головой. Очень разговорчивые и привязчивые.",
        "image": "ориентальская.jpg"  
    },
    {
        "id": 13,
        "breed": "Сибирская кошка",
        "description": "Сибирская кошка - российская порода полудлинношёрстных кошек. Имеет густую шерсть с водоотталкивающими свойствами, развитый охотничий инстинкт. Считается гипоаллергенной породой.",
        "image": "сибирская.jpg" 
    },
    {
        "id": 14,
        "breed": "Бирманская кошка",
        "description": "Бирманская кошка или Священная бирма - порода полудлинношёрстных кошек колор-пойнтового окраса с белыми 'носочками' на лапах. Согласно легенде, произошли от храмовых кошек Бирмы.",
        "image": "бирманская2.png"  
    },
    {
        "id": 15,
        "breed": "Девон-рекс",
        "description": "Девон-рекс - порода кошек с кудрявой шерстью, большими ушами и выразительными глазами. Шерсть мягкая, волнистая, почти не линяет. Очень активные, игривые и общительные кошки.",
        "image": "девон рекс.jpg" 
    },
    {
        "id": 16,
        "breed": "Турецкая ангора",
        "description": "Турецкая ангора - древняя порода кошек, происходящая из Турции. Чаще всего белого окраса с разноцветными глазами. Очень грациозные, активные и умные кошки с шелковистой шерстью.",
        "image": "турецкая.jpg"  
    },
    {
        "id": 17,
        "breed": "Египетская мау",
        "description": "Египетская мау - порода кошек, имеющая характерный пятнистый окрас. Это одна из немногих естественно пятнистых пород домашних кошек. Очень активные, преданные и обладают развитым охотничьим инстинктом.",
        "image": "египетская-мау.jpg" 
    },
    {
        "id": 18,
        "breed": "Корниш-рекс",
        "description": "Корниш-рекс - порода кошек с волнистой шерстью, образованной только подшёрстком. Тело стройное, изящное, с большими ушами. Очень активные, теплолюбивые и общительные кошки.",
        "image": "корниш-рекс.jpg" 
    },
    {
        "id": 19,
        "breed": "Манчкин",
        "description": "Манчкин - порода кошек с короткими лапами, возникшая в результате естественной генетической мутации. Несмотря на короткие лапы, они подвижны и активны. Характер дружелюбный и любознательный.",
        "image": "манчкин.jpg"  
    },
    {
        "id": 20,
        "breed": "Саванна",
        "description": "Саванна - гибрид домашней кошки и африканского сервала. Имеет экзотическую дикую внешность, высокие ноги и пятнистый окрас. Очень умные, активные, некоторые особи могут достигать веса 15 кг.",
        "image": "саванна.jpg"  
    }
]

@app.route('/lab2/cat_breeds')
def show_cat_breeds():
    return render_template('cat_breeds.html', cat_breeds=cat_breeds)