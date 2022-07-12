# %%
from email.mime import base
from unittest import result
from flask_sqlalchemy import SQLAlchemy
from app import app
from flask import render_template, send_file, Flask, jsonify
from app.models import InvoiceModel, ClientModel
from sqlalchemy import Boolean, create_engine, insert, select, func, distinct, true, values 
from sqlalchemy.orm import sessionmaker, declarative_base
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.backends.backend_template import FigureManagerTemplate
import base64
from io import StringIO, BytesIO
from matplotlib.figure import Figure
import seaborn as sns
import io
import psycopg2
import json

engine = create_engine('postgresql://postgres@localhost:5432/billit')
Session = sessionmaker(bind=engine)
session = Session()
# %%

#total_inv = session.query(InvoiceModel.paid).count()
paid_inv = session.query(InvoiceModel).filter(InvoiceModel.paid == True).count()
unpaid_inv = session.query(InvoiceModel).filter(InvoiceModel.paid == False).count()
total_inv = session.query(InvoiceModel).count()
# %%
'''x = ['Invoice Status']
paid = [paid_inv]
unpaid = [unpaid_inv] 
x_axis = np.arange(len(x))

plt.bar(x_axis - 0.1, paid, 0.3, label = 'Paid Invoices', color='green')
plt.bar(x_axis + 0.1, unpaid, 0.3, label = 'Unpaid Invoices', color='red')


plt.xticks(x_axis, x)
plt.ylabel('Number of Invoices')
plt.title('Number of Paid and Unpaid Invoices')
plt.legend()
plt.show()'''
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
plt.show()'''




'''sections = [paid_inv, unpaid_inv]
labels = ['Paid Invoices', 'Unpaid Invoices']
colors = ['green', 'red']
plt.title('Paid vs. Unpaid')
plt.pie(sections, labels=labels, wedgeprops={'edgecolor': 'black'}, colors=colors)
plt.savefig('app/static/images/invoice_payment_data.png')'''

#plt.savefig(img, format='png')
#img.seek(0)
#plot_url = base64.b64encode(img.getvalue()).decode()
#return '<img src="data:image/png;base64,{}">'.format(plot_url)


'''df = pd.DataFrame({
    'paid': [paid_inv], 
    'unpaid': [unpaid_inv],
    'total': [total_inv]})
ax = plt.subplot()
ax.bar(x = df['paid'], y = df['total'], color='green', height='55')
ax.bar(x = df['unpaid'], y = df['total'], color='red', height='55')
plt.show()'''


# %%

y = np.array([paid_inv, unpaid_inv])
data_labels = ['Paid Invoices', 'Unpaid Invoices']
explode_data = [0, 0.1]
sect_colors = ['gray', 'red']
plt.pie(y, labels=data_labels, explode=explode_data, colors=sect_colors)
plt.legend()
plt.savefig('app/static/img/invoice_payment_data.png')
plt.show()

# %%

list_paid = [paid_inv]
list_unpaid = [unpaid_inv]
list_total = ["Total Invoices"]

bottom_paid=list_unpaid

fig, ax = plt.subplots()
p1=ax.bar(list_total, list_unpaid)
p2=ax.bar(list_total, list_paid, bottom=bottom_paid)

plt.show()
# %%
'''fig = Figure()
gs = fig.add_gridspec(1, 2)
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
xs = range(q.paid_inv)
xs2 = range(q.unpaid_inv)
ys1 = range(q.total_inv)
ax1.hist(xs, ys1)
ax2.hist(xs2, ys1)
output = io.BytesIO()
FigureCanvas(fig).print_png(output)
return Response(output.getvalue(), mimetype='image/png')'''
# %%
conn = psycopg2.connect (
    """
    dbname=billit user=postgres host=localhost port=5432
    """
)
conn.set_session(autocommit=True)
cur = conn.cursor()
cur.execute(
    """
    SELECT state, COUNT(*) AS companies
	FROM clients GROUP BY state
	ORDER BY companies DESC LIMIT 10;
    """
)
records = json.dumps(cur.fetchall())
print(records)
# %%
conn = psycopg2.connect (
    """
    dbname=billit user=postgres host=localhost port=5432
    """
)
conn.set_session(autocommit=True)
cur = conn.cursor()
cur.execute(
    """
	SELECT SUM(invoices.amount) AS amount_spent, clients.company AS client_name
	FROM invoices
	INNER JOIN clients
	ON invoices.client = clients.id
	GROUP BY invoices.client, clients.company
	ORDER BY amount_spent DESC LIMIT 10;
    """
)
records = (cur.fetchall())
top_ten_spenders = []
for row in records:
    top_ten_spenders.append({"amount": (row[0]), "company": (row[1])})
results = json.dumps(top_ten_spenders)
print(results)


# %%
