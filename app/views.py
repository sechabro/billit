
from flask_sqlalchemy import SQLAlchemy
from app import app
from flask import render_template
from app.models import InvoiceModel, ClientModel
from sqlalchemy import Boolean, create_engine, insert, select, func, distinct, true, values 
from sqlalchemy.orm import sessionmaker, declarative_base, session

engine = create_engine('postgresql://postgres@localhost:5432/billit')
Session = sessionmaker(bind=engine)


@app.route('/')
def index_home():
    session = Session()
    paid_inv = session.query(InvoiceModel).filter(InvoiceModel.paid == True).count()
    unpaid_inv = session.query(InvoiceModel).filter(InvoiceModel.paid == False).count()
    total_clients = session.query(ClientModel).count()
    return render_template('public/index.html', paid_inv = paid_inv, unpaid_inv = unpaid_inv, total_clients = total_clients)
