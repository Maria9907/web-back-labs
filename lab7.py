from flask import Blueprint, render_template, request, abort, jsonify
from datetime import datetime

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')


films = [

    {
        "title":"You're driving me crazy",
        "title_ru": "Сводишь с ума",
        "year": 2025,
        "description": "Алиса заселяется в просторную квартиру в Санкт-Петербурге, \
        в которой начинает сбоить зеркало, показывая юной квартирантке \
        параллельную реальность той же самой квартиры. Вот только проживает \
        в этой параллельной реальности не Алиса, а тусовщик Иван.",
    },
    {
        "title":"Interstellar",
        "title_ru": "Интерстеллар",
        "year": 2014,
        "description": "Когда засуха, пыльные бури и вымирание растений \
        приводят человечество к продовольственному кризису, коллектив \
        исследователей и учёных отправляется сквозь червоточину \
        (которая предположительно соединяет области пространства-времени \
        через большое расстояние) в путешествие, чтобы превзойти прежние \
        ограничения для космических путешествий человека и найти планету с \
        подходящими для человечества условиями.",
    },
    {
        "title":"Beginning",
        "title_ru": "Начало",
        "year": 2010, 
        "description": "Кобб – талантливый вор, лучший из лучших в опасном \
        искусстве извлечения: он крадет ценные секреты из глубин подсознания \
        во время сна, когда человеческий разум наиболее уязвим. Редкие \
        способности Кобба сделали его ценным игроком в привычном к предательству \
        мире промышленного шпионажа, но они же превратили его в извечного беглеца \
        и лишили всего, что он когда-либо любил. Его последнее дело может вернуть \
        все назад, но для этого ему нужно совершить невозможное – инициацию. \
        Вместо идеальной кражи Кобб и его команда спецов должны будут \
        провернуть обратное.",
    },
]

def validate_film(film):
    errors = {}
    
    if not film.get('title_ru') or film['title_ru'].strip() == '':
        errors['title_ru'] = 'Русское название не может быть пустым'
    
    current_year = datetime.now().year
    try:
        year = int(film.get('year', 0))
        if year < 1895 or year > current_year:
            errors['year'] = f'Год должен быть в диапазоне от 1895 до {current_year}'
    except (ValueError, TypeError):
        errors['year'] = 'Год должен быть числом'
    
    description = film.get('description', '').strip()
    if not description:
        errors['description'] = 'Описание не может быть пустым'
    elif len(description) > 2000:
        errors['description'] = 'Описание не может превышать 2000 символов'
    
    return errors


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(films)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        abort(404)
    return films[id]

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id < 0 or id >= len(films):
        abort(404)
    del films[id]
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):
        abort(404)
    film = request.get_json()
    
    if not film.get('description') or film['description'].strip() == '':
        return {"description": "Описание не может быть пустым"}, 400
    
    errors = validate_film(film)
    if errors:
        return jsonify(errors), 400
    
    if (not film.get('title') or film['title'].strip() == '') and film.get('title_ru'):
        film['title'] = film['title_ru']

    films[id] = film
    return films[id]


@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_films():
    film = request.get_json()
    if not film:
        abort(400, description="No data provided")

    if not film.get('description') or film['description'].strip() == '':
        return {"description": "Описание не может быть пустым"}, 400
    
    errors = validate_film(film)
    if errors:
        return jsonify(errors), 400
    
    if (not film.get('title') or film['title'].strip() == '') and film.get('title_ru'):
        film['title'] = film['title_ru']
    
    films.append(film)
    return {"id": len(films) - 1}, 201
