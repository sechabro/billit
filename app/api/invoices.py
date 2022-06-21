from flask import Blueprint, jsonify, abort, redirect, request, render_template
import requests as req
import sqlalchemy
from ..models import InvoiceModel, db
from sqlalchemy import BOOLEAN, Boolean, create_engine, insert, select, func, distinct
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

'''@bp.route('/unpaid', methods=['GET'])
def get_unpaid():
    unpaid = InvoiceModel.query.filter(InvoiceModel.paid == False)
    unpaid_list = []
    for u in unpaid:
        unpaid_list.append(u.serialize())
    result = jsonify(unpaid_list)
    return result

for r in len(result):
        invoice_number = result['id']
        client = result['client']
        date_sent = result['date_sent']
        amount = result['amount']
        return invoice_number, client, date_sent, amount



@bp.route('/make-inv', methods=['GET', 'POST'])
def create_invoice():
    if request.method == 'POST':
        req = request.form
        return redirect(request.url)'''