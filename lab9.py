from flask import Blueprint, render_template
from flask import Blueprint, redirect, url_for, abort, session, make_response, request, render_template, current_app 
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path


lab9 = Blueprint('lab9', __name__)

@lab9.route('/lab9/')
def main():
    return render_template('lab9/index.html')
