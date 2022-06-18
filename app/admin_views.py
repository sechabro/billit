from flask_sqlalchemy import SQLAlchemy
from app import app
from flask import render_template, send_file, Flask, send_from_directory, Response
from app.models import InvoiceModel, ClientModel
from sqlalchemy import Boolean, create_engine, insert, select, func, distinct, true, values 
from sqlalchemy.orm import sessionmaker, declarative_base
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import base64
import random
#Connect
engine = create_engine('postgresql://postgres@localhost:5432/billit')
Session = sessionmaker(bind=engine)
session = Session()

#Dashboard invoice data
paid_inv = session.query(InvoiceModel).filter(InvoiceModel.paid == True).count()
unpaid_inv = session.query(InvoiceModel).filter(InvoiceModel.paid == False).count()
total_clients = session.query(ClientModel).count()
total_inv = session.query(InvoiceModel).count()



@app.route('/dashboard')
def dashboard_index():

    return render_template('admin/dashboard.html', paid_inv = paid_inv, unpaid_inv = unpaid_inv, total_inv=total_inv, total_clients = total_clients)


@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(paid_inv)
    ys1 = range(total_inv)
    axis.hist(xs, ys1)
    return fig
    
'''@app.route('/plot')
def build_plot():
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

@app.route('/pie_graph.png')
def invoice_pie():


def create_figure():
    sections = [paid_inv, unpaid_inv]
    labels = ['Paid Invoices', 'Unpaid Invoices']
    colors = ['green', 'red']
    fig1, ax1 = plt.subplots()
    ax1.title('Paid vs. Unpaid')
    ax1.pie(sections, labels=labels, wedgeprops={'edgecolor': 'black'}, colors=colors)
    ax1.axis('equal')
    plt.savefig('/static/images/invoice_payment_data.png')
    return send_from_directory(pie)'''