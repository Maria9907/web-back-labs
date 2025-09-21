from flask import Flask, url_for, request, redirect
import datetime

app = Flask(__name__)


from flask import abort


@app.errorhandler(404)
def not_found(err):
    css_path = url_for("static", filename="lab1.css")
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
        <p><a href="/">Вернуться на главную</a></p>
    </div>
</body>
</html>""",
        404,
    )


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
    return (
        f'''
<!doctype html> 
<html>
    <head>
        <title>Природа</title>
        <link rel="stylesheet" type="text/css" href="{css_path}">
    </head>
    <body>
        <h1>Природа</h1>
        <img src="'''
        + path
        + """">
    </body>
</html>
"""
    )


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
    return """
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
    <body>
</html>
"""
