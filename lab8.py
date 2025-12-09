from flask import Blueprint, render_template, request, abort, jsonify, current_app
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

lab7 = Blueprint('lab8', __name__)

