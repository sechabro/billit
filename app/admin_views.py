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

#Connect
engine = create_engine('postgresql://postgres@localhost:5432/billit')
Session = sessionmaker(bind=engine)
session = Session()

#Dashboard invoice data
paid_inv = session.query(InvoiceModel).filter(InvoiceModel.paid == True).count()
unpaid_inv = session.query(InvoiceModel).filter(InvoiceModel.paid == False).count()
total_clients = session.query(ClientModel).count()
total_inv = session.query(InvoiceModel).count()
billed_total_query = session.query(func.sum(InvoiceModel.amount))
billed_total = round(billed_total_query.scalar(), 2)
collected_total_query = session.query(func.sum(InvoiceModel.amount)).filter(InvoiceModel.paid == True)
collected_total = round(collected_total_query.scalar(), 2)


@app.route('/dashboard')
def dashboard_index():

    return render_template('admin/dashboard.html', paid_inv = paid_inv, unpaid_inv = unpaid_inv, total_inv=total_inv,
    total_clients = total_clients, billed_total=billed_total, collected_total=collected_total)

@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig = Figure()
    gs = fig.add_gridspec(1, 2)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    xs = range(paid_inv)
    xs2 = range(unpaid_inv)
    ys1 = range(total_inv)
    ax1.hist(xs, ys1)
    ax2.hist(xs2, ys1)
    return fig
    
