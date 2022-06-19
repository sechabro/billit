# %%
from email.mime import base
from flask_sqlalchemy import SQLAlchemy
from app import app
from flask import render_template, send_file, Flask
from app.models import InvoiceModel, ClientModel
from sqlalchemy import Boolean, create_engine, insert, select, func, distinct, true, values 
from sqlalchemy.orm import sessionmaker, declarative_base
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigCan
from matplotlib.backends.backend_template import FigureManagerTemplate
import base64, io
from matplotlib.figure import Figure
import seaborn as sns
engine = create_engine('postgresql://postgres@localhost:5432/billit')
Session = sessionmaker(bind=engine)
session = Session()
# %%

#total_inv = session.query(InvoiceModel.paid).count()
paid_inv = session.query(InvoiceModel).filter(InvoiceModel.paid == True).count()
unpaid_inv = session.query(InvoiceModel).filter(InvoiceModel.paid == False).count()
total_inv = session.query(InvoiceModel).count()
# %%
x = ['Invoice Status']
paid = [paid_inv]
unpaid = [unpaid_inv] 
x_axis = np.arange(len(x))

plt.bar(x_axis - 0.1, paid, 0.3, label = 'Paid Invoices', color='green')
plt.bar(x_axis + 0.1, unpaid, 0.3, label = 'Unpaid Invoices', color='red')


plt.xticks(x_axis, x)
plt.ylabel('Number of Invoices')
plt.title('Number of Paid and Unpaid Invoices')
plt.legend()
plt.show()
# %%
'''fig, ax = plt.subplots(figsize=(6,6))
ax = sns.set_style(style='darkgrid')
x = [i for i in range(100)]
y = [i for i in range(100)]
sns.lineplot(x,y)
canvase = FigCan(fig)
img = io.BytesIO()
fig.savefig(img)
img.seek(0)
#Pie graphing total_inv
sections = [paid_inv, unpaid_inv]
labels = ['Paid Invoices', 'Unpaid Invoices']
colors = ['green', 'red']
plt.title('Paid vs. Unpaid')
plt.pie(sections, labels=labels, wedgeprops={'edgecolor': 'black'}, colors=colors)
plt.axis('equal')
#plt.savefig('app/static/images/invoice_payment_data.png')
plt.show()



img = io.BytesIO()
sections = [paid_inv, unpaid_inv]
labels = ['Paid Invoices', 'Unpaid Invoices']
colors = ['green', 'red']
plt.title('Paid vs. Unpaid')
plt.pie(sections, labels=labels, wedgeprops={'edgecolor': 'black'}, colors=colors)
plt.savefig(img, format='png')
img.seek(0)
plot_url = base64.b64encode(img.getvalue()).decode()
return '<img src="data:image/png;base64,{}">'.format(plot_url)


df = pd.DataFrame({
    'paid': [paid_inv], 
    'unpaid': [unpaid_inv],
    'total': [total_inv]})
ax = plt.subplot()
ax.bar(x = df['paid'], y = df['total'], color='green', height='55')
ax.bar(x = df['unpaid'], y = df['total'], color='red', height='55')
plt.show()'''
