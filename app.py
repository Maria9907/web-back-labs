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
        <nav>
            <a href="/lab1">Первая лабораторная</a>
        </nav>
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


flower_list = ["роза", "тюльпан", "незабудка", "ромашка"]


@app.route("/lab2/flowers/<int:flower_id>")
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    return f"""
<!doctype html>
<html>
    <head>
        <title>Цветок #{flower_id}</title>
    </head>
    <body>
        <h1>Информация о цветке</h1>
        <p>ID цветка: {flower_id}</p>
        <p>Название: {flower_list[flower_id]}</p>
        <a href="{url_for('show_all_flowers')}">Посмотреть все цветы</a>
    </body>
</html>
"""


@app.route("/lab2/add_flower/")
def add_flower_no_name():
    response = make_response("вы не задали имя цветка", 400)
    return response


@app.route("/lab2/add_flower/<name>")
def add_flower(name):
    flower_list.append(name)
    return f"""
<!doctype html> 
<html>
    <body>
    <h1>Добавлен новый цветок</h1>
    <p>Название нового цветка: {name} </p>
    <p>Всего цветков: {len(flower_list)} </p>
    <p>Полный список: {flower_list} </p>
    </body>
</html>
"""


@app.route("/lab2/all_flowers")
def show_all_flowers():
    num_flowers = len(flower_list)
    return f"Всего цветов: {num_flowers}\nСписок цветов: {', '.join(flower_list)}"

@app.route("/lab2/clear")
def clear_flowers():
    flower_list.clear()
    return f"""
<!doctype html>
<html>
    <head>
        <title>Список очищен</title>
    </head>
    <body>
        <h1>Список цветов очищен!</h1>
        <p>Все цветы были удалены из коллекции.</p>
        <a href="{url_for('show_all_flowers')}">Вернуться к списку цветов</a>
    </body>
</html>
"""

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
