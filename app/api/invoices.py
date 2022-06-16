from flask import Blueprint, jsonify, abort, request
import requests as req
import sqlalchemy
from ..models import InvoiceModel, db
from sqlalchemy import create_engine, insert, select, func, distinct
from sqlalchemy.orm import sessionmaker, declarative_base, session
from datetime import datetime, date
import psycopg2
import pytz

bp = Blueprint('invoices', __name__, url_prefix='/invoices')

#Connecting to local database
engine = create_engine('postgresql://postgres@localhost:5432/billit')
Session = sessionmaker(bind=engine)
Base = declarative_base()

@bp.route('', methods=['GET']) # decorator takes path and list of HTTP verbs
def client_index():
    invoices = InvoiceModel.query.all() # ORM performs SELECT query
    result = []
    for i in invoices:
        result.append(i.serialize()) # appending results to result list
    return jsonify(result) # return JSON response



