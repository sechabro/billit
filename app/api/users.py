from flask import Blueprint, jsonify, abort, redirect, request, render_template, make_response
import requests as req
import sqlalchemy
from ..models import UserModel, db
from sqlalchemy import BOOLEAN, Boolean, create_engine, insert, select, func, distinct
from sqlalchemy.orm import sessionmaker, declarative_base, session
from datetime import datetime, date
import psycopg2
import pytz

bp = Blueprint('users', __name__, url_prefix='/users')

# Connecting to local database
engine = create_engine('postgresql://postgres@localhost:5432/billit')
Session = sessionmaker(bind=engine)
Base = declarative_base()


@bp.route('', methods=['GET'])  # decorator takes path and list of HTTP verbs
def client_index():
    invoices = UserModel.query.all()  # ORM performs SELECT query
    result = []
    for i in invoices:
        result.append(i.serialize())  # appending results to result list
    return jsonify(result)  # return JSON response
