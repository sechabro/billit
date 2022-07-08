from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import ForeignKey, create_engine, Column, Integer, String, Boolean
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import time

db = SQLAlchemy()
engine = create_engine('postgresql://postgres@localhost:5432/billit')
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Reference:
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
# https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Column
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/#many-to-many-relationships


class InvoiceModel(db.Model):
    __tablename__ = 'invoices'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client = db.Column(db.Integer, ForeignKey('clients.id'), nullable=False)
    date_sent = db.Column(db.Date, nullable=True)
    date_paid = db.Column(db.Date, nullable=True)
    services = db.Column(db.Text, nullable=True)
    amount = db.Column(db.Float, nullable=False)
    paid = db.Column(db.Boolean, nullable=False)

    def __init__(self, id, client, date_sent, date_paid, services, amount, paid):
        self.id = id
        self.client = client
        self.date_sent = date_sent
        self.date_paid = date_paid
        self.services = services
        self.amount = amount
        self.paid = paid

    def serialize(self):
        return {
            'id': self.id,
            'client': self.client,
            'date_sent': self.date_sent, #.isoformat(),
            'date_paid': self.date_paid, #.isoformat(),
            'services': self.services,
            'amount': self.amount,
            'paid': self.paid
        }


class ClientModel(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company = db.Column(db.Text, nullable=False)
    contact = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=True)
    address = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(128), nullable=False)
    state = db.Column(db.String(128), nullable=False)
    zipcode = db.Column(db.String(), nullable=False)

    def __init__(self, id, company, contact, email, address, city, state, zipcode):
        self.id = id
        self.company = company
        self.contact = contact
        self.email = email
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode

    def serialize(self):
        return {
            'id': self.id,
            'company': self.company,
            'contact': self.contact,
            'email': self.email,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zipcode': self.zipcode
        }
