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
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
app = Flask(__name__)
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)


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
            <li>
                <a href="/lab3">Третья лабораторная работа</a>
            </li>
        </ul>
            
        <footer>
            <p>Матюшкина Мария Дмитриевна, ФБИ-32, 3 курс, 2025 год</p>
        </footer>
    </body>
</html>
"""

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

    css_path = url_for("static", filename="lab1/lab1.css")

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

