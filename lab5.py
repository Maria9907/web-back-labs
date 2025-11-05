from flask import Blueprint, redirect, url_for, abort, session, make_response, request, render_template

lab5 = Blueprint('lab5',__name__)

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html')

@lab5.route('/lab5/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('lab5/register.html', error='Заполните все поля')



