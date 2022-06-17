# %%
from flask_sqlalchemy import SQLAlchemy
from app import app
from flask import render_template, send_file
from app.models import InvoiceModel, ClientModel
from sqlalchemy import Boolean, create_engine, insert, select, func, distinct, true, values 
from sqlalchemy.orm import sessionmaker, declarative_base
import numpy as np, pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigCan
import base64, io
engine = create_engine('postgresql://postgres@localhost:5432/billit')
Session = sessionmaker(bind=engine)
session = Session()
# %%

#total_inv = session.query(InvoiceModel.paid).count()
paid_inv = session.query(InvoiceModel).filter(InvoiceModel.paid == True).count()
unpaid_inv = session.query(InvoiceModel).filter(InvoiceModel.paid == False).count()

# %%
#Pie graphing total_inv
sections = [paid_inv, unpaid_inv]
labels = ['Paid Invoices', 'Unpaid Invoices']
colors = ['green', 'red']
plt.title('Paid vs. Unpaid')
pie = plt.pie(sections, labels=labels, wedgeprops={'edgecolor': 'black'}, colors=colors)
pie
#<img src="{{ url_for('invoice_pie') }}">
# %%
