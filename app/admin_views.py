from multiprocessing.connection import Client
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
import pprint

pp = pprint.PrettyPrinter(indent=2, width=160, compact=False)

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

@app.route('/dashboard/by-client', methods=['GET', 'POST'])
def client_view():
    clients = InvoiceModel.query.order_by(InvoiceModel.client)
    client_list = []
    for c in clients:
        client_list.append(c.serialize())
    #client_select = ClientModel.query.all()
    #client_list = []
    #for c in client_select:
    #    client_list.append(c.serialize())
    return render_template('admin/by-client.html', client_list=client_list, paid_inv=paid_inv, unpaid_inv=unpaid_inv, total_inv=total_inv,
                           total_clients=total_clients, billed_total=billed_total, collected_total=collected_total)


@app.route('/dashboard/inv-prepop/<int:inv_id>', methods=['GET', 'POST'])
def inv_passthrough(inv_id: int):
    inv = InvoiceModel.query.filter(InvoiceModel.id == inv_id)
    if request.method == 'POST':
        inv_to_update = []
        for i in inv:
            inv_to_update.append(i.serialize())
        #invoice = inv_to_update[0]['id']
        client_id = inv_to_update[0]['client']

        client_select = ClientModel.query.all()
        client_list = []
        for c in client_select:
            client_list.append(c.serialize())

        unpaid = InvoiceModel.query.filter(InvoiceModel.paid == False)
        unpaid_list = []
        for u in unpaid:
            unpaid_list.append(u.serialize())

        return render_template('admin/update.html', client_id=client_id, inv_to_update=inv_to_update, unpaid_list=unpaid_list, client_list=client_list, total_clients=total_clients, paid_inv=paid_inv, unpaid_inv=unpaid_inv, total_inv=total_inv,
                               billed_total=billed_total, collected_total=collected_total)


@app.route('/dashboard/del-prepop/<int:inv_id>', methods=['GET', 'POST'])
def delete_inv_passthrough(inv_id: int):
    inv = InvoiceModel.query.filter(InvoiceModel.id == inv_id)
    if request.method == 'POST':
        inv_to_delete = []
        for i in inv:
            inv_to_delete.append(i.serialize())
        client_id = inv_to_delete[0]['client']

        client_select = ClientModel.query.filter(
            ClientModel.id == int(client_id))
        client_info = []
        for c in client_select:
            client_info.append(c.serialize())
        return render_template('admin/delete.html', client_info=client_info, inv_to_delete=inv_to_delete)
    else:
        print('No request sent.')


@app.route('/delete-inv', methods=['GET', 'POST'])
def delete_invoice():
    if request.method == 'POST':
        req = request.get_json()
        int_req = int(req['inv_id'])
        inv = InvoiceModel.query.filter(InvoiceModel.id == int_req)
        pp.pprint(req)
        pp.pprint(int(req['inv_id']))

        try:
            db.session.delete(inv)
            db.session.commit()
            flash('Invoice deleted successfully.')
            return jsonify({'status': 'invoice deleted'})
            # return redirect(url_for('unpaid_view'))
        except:
            flash('Failed to delete invoice!')
            return jsonify({'status': 'error: invoice not deleted.'})
            # return redirect(url_for('unpaid_view'))
    else:
        print('NOT A POST :(')
        return 'REQUEST FAILED'


@app.route('/update-inv', methods=['GET', 'POST'])
def update_invoice():
    if request.method == 'POST':
        req = request.get_json()
        pp.pprint(req)
        pp.pprint(req['amount'])
        return jsonify({'status': 'looking good'})
    else:
        print('NOT A POST :(')
        return 'REQUEST FAILED'
        '''client_id = request.form['client_id']
        inv_id = request.form['inv_id']
        amount = request.form['amount']
        services = request.form['services']
        paid = request.form['paid']
        print(client_id, inv_id, amount, services, paid)'''





@app.route('/inv-form-return', methods=['GET', 'POST'])
def inv_form():
    client_select = ClientModel.query.all()
    client_list = []
    for c in client_select:
        client_list.append(c.serialize())
    return render_template('admin/make-inv.html', client_list=client_list)

@app.route('/create-inv', methods=['GET', 'POST'])
def create_invoice():
    if request.method == 'POST':
        req = request.get_json()
        pp.pprint(req)
        pp.pprint(req['amount'])
        return jsonify({'status': 'looking good'})
    else:
        print('NOT A POST :(')
        return 'REQUEST FAILED'





@app.route('/client-form-return', methods=['GET', 'POST'])
def client_form():
    states = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']
    return render_template('admin/add-client.html', states=states)

@app.route('/add-client', methods=['GET', 'POST'])
def add_client():
    if request.method == 'POST':
        req = request.get_json()
        pp.pprint(req)
        return jsonify({'status': 'looking good'})
    else:
        print('NOT A POST :(')
        return 'REQUEST FAILED'



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
