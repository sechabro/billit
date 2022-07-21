from multiprocessing.connection import Client
from flask_sqlalchemy import SQLAlchemy
from app import app
from flask import Blueprint, flash, jsonify, make_response, redirect, render_template, send_file, Flask, send_from_directory, Response, url_for, request, session as sesh
from app.models import InvoiceModel, ClientModel, UserModel, db
from sqlalchemy import Boolean, create_engine, insert, select, func, distinct, true, values, delete, update
from sqlalchemy.orm import sessionmaker, declarative_base
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import json
import pprint
import psycopg2

pp = pprint.PrettyPrinter(indent=2, width=160, compact=False)

# Connect
engine = create_engine('postgresql://postgres@localhost:5432/billit')
Session = sessionmaker(bind=engine)
session = Session()

# DASHBOARD QUERIES


class Queries:
    def gen_query(self):
        self.paid_inv = session.query(InvoiceModel).filter(InvoiceModel.paid == True).count()
        self.unpaid_inv = session.query(InvoiceModel).filter(InvoiceModel.paid == False).count()
        self.total_clients = session.query(ClientModel).count()
        self.total_inv = session.query(InvoiceModel).count()
        self.billed_total_query = session.query(func.sum(InvoiceModel.amount))
        self.collected_total_query = session.query(func.sum(InvoiceModel.amount)).filter(InvoiceModel.paid == True)
        self.billed_total = round(self.billed_total_query.scalar(), 2)
        self.collected_total = round(self.collected_total_query.scalar(), 2)

    def list(self, arg):  # This function creates a list out of all queries within methods
        list = []
        for i in arg:
            list.append(i.serialize())
        return list

    # LOGIN CHECK ------------------------------------
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            req = request.get_json()
            user = req['username']
            user_query = UserModel.query.filter(UserModel.name == user)
            user_record = q.list(user_query)
            if user == user_record['name']:
                pwd = req['password']
                if pwd == user_record['password']:
                    sesh['user'] = user
                    return redirect(url_for('invoice_index'))
                else:
                    flash('Invalid username-password combination.')
                    return render_template('public/index.html')
            else:
                flash('Invalid username.')
                return render_template('public/index.html')
        else:
            flash('Please login.')
            return render_template('public/index.html')
    #---------------------------------------------------

    # TEMPLATE BASE ----------------

    @app.route('/dashboard')
    def dashboard_index():
        return render_template('admin/templates/dashboard_template.html', paid_inv=q.paid_inv, unpaid_inv=q.unpaid_inv, total_inv=q.total_inv,
                               total_clients=q.total_clients, billed_total=q.billed_total, collected_total=q.collected_total)
    # ------------------------------
    # DASHBOARD SORT VIEWS -----------------------------

    @app.route('/dashboard/all', methods=['GET', 'POST'])
    def invoice_index():
        if 'user' in sesh:
            user = sesh['user']
            q.gen_query()
            invoices = session.query(InvoiceModel).order_by(InvoiceModel.id)
            client_select = ClientModel.query.all()
            invoice_list = q.list(invoices)
            client_list = q.list(client_select)
            return render_template('admin/all.html', user=user, invoice_list=invoice_list, client_list=client_list, paid_inv=q.paid_inv, unpaid_inv=q.unpaid_inv, total_inv=q.total_inv,
                                   total_clients=q.total_clients, billed_total=q.billed_total, collected_total=q.collected_total)
        else:
            flash('Please login.')
            return render_template('public/index.html')

    @app.route('/dashboard/unpaid', methods=['GET', 'POST'])
    def unpaid_view():
        q.gen_query()
        unpaid = InvoiceModel.query.filter(InvoiceModel.paid == False)
        client_select = ClientModel.query.all()
        unpaid_list = q.list(unpaid)
        client_list = q.list(client_select)
        return render_template('admin/unpaid.html', client_list=client_list, unpaid_list=unpaid_list, paid_inv=q.paid_inv, unpaid_inv=q.unpaid_inv, total_inv=q.total_inv,
                               total_clients=q.total_clients, billed_total=q.billed_total, collected_total=q.collected_total)

    @app.route('/dashboard/by-client', methods=['GET', 'POST'])
    def client_view():
        q.gen_query()
        clients = InvoiceModel.query.order_by(InvoiceModel.client)
        client_list = q.list(clients)
        return render_template('admin/by-client.html', client_list=client_list, paid_inv=q.paid_inv, unpaid_inv=q.unpaid_inv, total_inv=q.total_inv,
                               total_clients=q.total_clients, billed_total=q.billed_total, collected_total=q.collected_total)
    # ---------------------------------------------

    # INVOICE ADDING, EDITING, AND DELETING ---------

    @app.route('/inv-form-return', methods=['GET', 'POST'])
    def inv_form():
        client_select = ClientModel.query.all()
        client_list = q.list(client_select)

        return render_template('admin/make-inv.html', client_list=client_list)

    @app.route('/create-inv', methods=['GET', 'POST'])
    def create_invoice():
        if request.method == 'POST':
            req = request.get_json()
            print('Creating invoice file for:', req)
            stmt = insert(InvoiceModel).values(client=req['client_id'], services=req['services'], amount=req['amount'],
                                               paid=req['paid'], date_paid=req['date_paid'], date_sent=req['date_sent'])
            with engine.connect() as conn:
                conn.execute(stmt)
            return jsonify({'Status': 'Client added!'})
        else:
            print('NOT A POST :(')
            return 'REQUEST FAILED'

    @app.route('/dashboard/inv-prepop/<int:inv_id>', methods=['GET', 'POST'])
    def inv_passthrough(inv_id: int):
        inv = InvoiceModel.query.filter(InvoiceModel.id == inv_id)
        if request.method == 'POST':
            inv_to_update = q.list(inv)
            client_id = inv_to_update[0]['client']
            client_select = ClientModel.query.all()
            client_list = q.list(client_select)
            return render_template('admin/update.html', client_id=client_id, inv_to_update=inv_to_update, client_list=client_list)
        else:
            print('NOT A POST :(')
            return 'REQUEST FAILED'

    @app.route('/update-inv', methods=['GET', 'POST'])
    def update_invoice():
        if request.method == 'POST':
            req = request.get_json()
            company = req['company']
            client_company = ClientModel.query.filter(
                ClientModel.company == company)
            client_info = q.list(client_company)
            stmt = update(InvoiceModel).where(InvoiceModel.id == req['inv_id']).values(client=client_info[0]['id'], amount=req['amount'], services=req['services'],
                                                                                       date_sent=req['date_sent'], date_paid=req['date_paid'], paid=req['paid'])
            with engine.connect() as conn:
                conn.execute(stmt)
            return jsonify({'Status': 'Invoice Updated'})
        else:
            print('NOT A POST :(')
            return 'REQUEST FAILED'

    @app.route('/dashboard/del-prepop/<int:inv_id>', methods=['GET', 'POST'])
    def delete_inv_passthrough(inv_id: int):
        inv = InvoiceModel.query.filter(InvoiceModel.id == inv_id)
        if request.method == 'POST':
            inv_to_delete = q.list(inv)
            client_id = inv_to_delete[0]['client']
            client_select = ClientModel.query.filter(
                ClientModel.id == int(client_id))
            client_info = q.list(client_select)
            return render_template('admin/delete.html', client_info=client_info, inv_to_delete=inv_to_delete)
        else:
            print('No request sent.')

    @app.route('/delete-inv', methods=['GET', 'POST'])
    def delete_invoice():
        if request.method == 'POST':
            req = request.get_json()
            int_req = int(req['inv_id'])
            try:
                stmt = delete(InvoiceModel).where(InvoiceModel.id == int_req)
                with engine.connect() as conn:
                    conn.execute(stmt)
                flash('Invoice deleted successfully.')
                return jsonify({'status': 'invoice deleted'})
            except:
                flash('Failed to delete invoice!')
                return jsonify({'status': 'error: invoice not deleted.'})
                # return redirect(url_for('unpaid_view'))

        else:
            print('NOT A POST :(')
            return 'REQUEST FAILED'
    # ---------------------------------------------

    # CLIENT ADDING, EDITING, AND DELETING ---------

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
            print('Creating client file for:', req)
            stmt = insert(ClientModel).values(company=req['company'], contact=req['contact'], email=req['email'],
                                              address=req['address'], city=req['city'], state=req['state'], zipcode=req['zipcode'])
            with engine.connect() as conn:
                conn.execute(stmt)
            return jsonify({'Status': 'Client added!'})
        else:
            print('NOT A POST :(')
            return 'REQUEST FAILED'
    # -------------------------------------




    # --------------- FIGURE GENERATION *NOT YET FUNCTIONAL* --------------------
    #@app.route('/plot.png')
    def pie_png(self):
        y = np.array([q.paid_inv, q.unpaid_inv])
        data_labels = ['Paid Invoices', 'Unpaid Invoices']
        explode_data = [0, 0.1]
        sect_colors = ['gray', 'red']
        plt.pie(y, labels=data_labels, explode=explode_data, colors=sect_colors)
        plt.legend()
        plt.switch_backend('png')
        plt.savefig('app/static/img/invoice_payment_data.png')


    #@app.route('/top_ten_spenders.png')
    def tts_png(self):
        q.gen_query()
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
        records = cur.fetchall()
        top_ten_spenders = []
        for row in records:
            top_ten_spenders.append({"amount": (row[0]), "company": (row[1])})
        return True
    #----------------------------------------------------------


q = Queries()
