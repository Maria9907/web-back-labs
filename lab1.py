from flask import Blueprint, redirect, url_for, abort, make_response, request
from datetime import datetime

lab1 = Blueprint('lab1',__name__)



@lab1.route("/lab1/400")
def route_bad_request():
    abort(400, description="Неправильный, некорректный запрос")


@lab1.route("/lab1/401")
def route_unauthorized():
    abort(401, description="Не авторизован")


@lab1.route("/lab1/403")
def route_forbidden():
    abort(403, description="Запрещено (не уполномочен)")


@lab1.route("/lab1/405")
def route_method_not_allowed():
    abort(405, description="Метод не поддерживается")


@lab1.route("/lab1/418")
def route_teapot():
    abort(418, description="Я - чайник")


@lab1.route("/lab1/")
def lab():
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


@lab1.route("/lab1/web")
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


@lab1.route("/lab1/author")
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


@lab1.route("/lab1/image")
def image():
    path = url_for("static", filename="lab1/картинка.jpg")
    css_path = url_for("static", filename="lab1/lab1.css")
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


count = 0  # Глобальная переменная для счетчика


@lab1.route("/lab1/counter")
def counter():
    global count
    count += 1
    time = datetime.now()
    url = request.url
    client_ip = request.remote_addr
    
    html_content = f"""
<!doctype html> 
<html>
    <body>
        Сколько раз вы сюда заходили: {count}
        <hr>
        Дата и время: {time}<br>
        запрошенный адрес: {url}<br>
        Ваш IP-адрес: {client_ip}<br>
        <a href="/lab1/clear_counter">Очистить счетчик</a>
    </body>
</html>
"""
    return html_content


@lab1.route("/lab1/clear_counter")
def clear_counter():
    global count
    count = 0
    return redirect("/lab1/counter")



@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")


@lab1.route("/created")
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



@lab1.route("/lab1/error")
def cause_error():
    try:
        result = 1 / 0
    except Exception as e:
        print(f"An error occurred: {e}")
        abort(500)
    return "Ошибка"

