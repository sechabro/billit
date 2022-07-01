from flask_sqlalchemy import SQLAlchemy
from app import app
from flask import Blueprint, flash, jsonify, make_response, redirect, render_template, send_file, Flask, send_from_directory, Response, url_for, request
from app.models import InvoiceModel, ClientModel, db
from sqlalchemy import Boolean, create_engine, insert, select, func, distinct, true, values, delete
from sqlalchemy.orm import sessionmaker, declarative_base
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import json

#bp = Blueprint('invoices', __name__, url_prefix='/dashboard')

# Connect
engine = create_engine('postgresql://postgres@localhost:5432/billit')
Session = sessionmaker(bind=engine)
session = Session()

# Dashboard data
paid_inv = session.query(InvoiceModel).filter(
    InvoiceModel.paid == True).count()
unpaid_inv = session.query(InvoiceModel).filter(
    InvoiceModel.paid == False).count()
total_clients = session.query(ClientModel).count()

total_inv = session.query(InvoiceModel).count()
billed_total_query = session.query(func.sum(InvoiceModel.amount))
billed_total = round(billed_total_query.scalar(), 2)
collected_total_query = session.query(
    func.sum(InvoiceModel.amount)).filter(InvoiceModel.paid == True)
collected_total = round(collected_total_query.scalar(), 2)





@app.route('/dashboard')
def dashboard_index():
    return render_template('admin/templates/dashboard_template.html', paid_inv=paid_inv, unpaid_inv=unpaid_inv, total_inv=total_inv,
                           total_clients=total_clients, billed_total=billed_total, collected_total=collected_total)






@app.route('/dashboard/all', methods=['GET', 'POST'])
def invoice_index():
    invoices = InvoiceModel.query.all()
    invoice_list = []
    for i in invoices:
        invoice_list.append(i.serialize())
    client_select = ClientModel.query.all()
    client_list = []
    for c in client_select:
        client_list.append(c.serialize())
    return render_template('admin/all.html', invoice_list=invoice_list, client_list=client_list, paid_inv=paid_inv, unpaid_inv=unpaid_inv, total_inv=total_inv,
                           total_clients=total_clients, billed_total=billed_total, collected_total=collected_total)





@app.route('/dashboard/unpaid', methods=['GET', 'POST'])
def unpaid_view():
    unpaid = InvoiceModel.query.filter(InvoiceModel.paid == False)
    unpaid_list = []
    for u in unpaid:
        unpaid_list.append(u.serialize())
    client_select = ClientModel.query.all()
    client_list = []
    for c in client_select:
        client_list.append(c.serialize())
    return render_template('admin/unpaid.html', client_list=client_list, unpaid_list=unpaid_list, paid_inv=paid_inv, unpaid_inv=unpaid_inv, total_inv=total_inv,
                           total_clients=total_clients, billed_total=billed_total, collected_total=collected_total)





@app.route('/dashboard/inv-prepop/<int:inv_id>', methods=['GET', 'POST'])
def inv_passthrough(inv_id: int):
    inv = InvoiceModel.query.filter(InvoiceModel.id == inv_id)
    inv_to_update = []
    for i in inv:
        inv_to_update.append(i.serialize())
    invoice = inv_to_update[0]['id']
    client_id = inv_to_update[0]['client']

    client_select = ClientModel.query.all()
    client_list = []
    for c in client_select:
        client_list.append(c.serialize())

    unpaid = InvoiceModel.query.filter(InvoiceModel.paid == False)
    unpaid_list = []
    for u in unpaid:
        unpaid_list.append(u.serialize())

    return render_template('admin/update_inv.html', client_id=client_id, inv_to_update=inv_to_update, unpaid_list=unpaid_list, client_list=client_list, total_clients=total_clients, paid_inv=paid_inv, unpaid_inv=unpaid_inv, total_inv=total_inv,
                           billed_total=billed_total, collected_total=collected_total)





@app.route('/dashboard/delete/<int:inv_id>', methods=['GET', 'POST'])
def delete_invoice(inv_id: int):
    inv = InvoiceModel.query.get_or_404(inv_id)
    if request == 'POST':
        try:
            db.session.delete(inv)
            db.session.commit()
            flash('Invoice deleted successfully.')
            return redirect(url_for('unpaid_view'))
        except:
            flash('Failed to delete invoice!')
            return redirect(url_for('unpaid_view'))





@app.route('/make-inv', methods=['GET', 'POST'])
def make_inv():
    return render_template('admin/make-inv.html', paid_inv=paid_inv, unpaid_inv=unpaid_inv, total_inv=total_inv,
                           total_clients=total_clients, billed_total=billed_total, collected_total=collected_total)





@app.route('/add-client', methods=['GET', 'POST'])
def add_client():
    return render_template('admin/add-client.html', paid_inv=paid_inv, unpaid_inv=unpaid_inv, total_inv=total_inv,
                           total_clients=total_clients, billed_total=billed_total, collected_total=collected_total)





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
