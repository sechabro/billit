from flask_sqlalchemy import SQLAlchemy
from app import app
from flask import render_template, send_file
from app.models import InvoiceModel, ClientModel
from sqlalchemy import Boolean, create_engine, insert, select, func, distinct, true, values 
from sqlalchemy.orm import sessionmaker, declarative_base
from matplotlib import pyplot as plt
import io
import base64

engine = create_engine('postgresql://postgres@localhost:5432/billit')
Session = sessionmaker(bind=engine)

@app.route('/dashboard')
def dashboard_index():
    session = Session()
    #Database Queries
    paid_inv = session.query(InvoiceModel).filter(InvoiceModel.paid == True).count()
    unpaid_inv = session.query(InvoiceModel).filter(InvoiceModel.paid == False).count()
    total_clients = session.query(ClientModel).count()
    return render_template('admin/dashboard.html', paid_inv = paid_inv, unpaid_inv = unpaid_inv, total_clients = total_clients)

'''@app.route('/invoice_pie')
def invoice_pie():
    session = Session()
    paid_inv = session.query(InvoiceModel).filter(InvoiceModel.paid == True).count()
    unpaid_inv = session.query(InvoiceModel).filter(InvoiceModel.paid == False).count()
    #Pie Graph
    sections = [paid_inv, unpaid_inv]
    labels = ['Paid Invoices', 'Unpaid Invoices']
    colors = ['green', 'red']
    pie = plt.pie(sections, labels=labels, wedgeprops={'edgecolor': 'black'}, colors=colors)
    return send_file(pie, mimetype='img/png')'''