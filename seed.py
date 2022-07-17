from faker import Faker
from flask import jsonify
import requests
from datetime import datetime
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker, declarative_base
from app.api.clients import ClientModel
from app.api.invoices import InvoiceModel

fake = Faker()

engine = create_engine('postgresql://postgres@localhost:5432/billit')
Session = sessionmaker(bind=engine)
Base = declarative_base()

'''companies = 80
for i in range(companies):
    company_name = fake.company()
    contact_name = fake.name()
    emails = fake.ascii_safe_email()
    addresses = fake.street_address()
    cities = fake.city()
    states = fake.random_elements(elements=('AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
                                            'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
                                            'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
                                            'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
                                            'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY'), length=1, unique=False)
    zipcodes = fake.postcode()
    stmt = insert(ClientModel).values(company=company_name, contact=contact_name,
                                      email=emails, address=addresses, city=cities, state=states, zipcode=zipcodes)
    with engine.connect() as conn:
        conn.execute(stmt)'''

invoices = 125
for i in range(invoices):
    clients = fake.random_int(min=1, max=80)
    dates_sent = fake.date_between(start_date='-45d', end_date='-30d')
    dates_paid = fake.date_between(start_date='-29d', end_date='-1d')
    amounts = fake.pydecimal(
        left_digits=4, right_digits=2, positive=True, min_value=100.00)
    services_rendered = fake.sentence(nb_words=12, variable_nb_words=True)
    paid_bills = fake.boolean(chance_of_getting_true=65)
    stmt = insert(InvoiceModel).values(client=clients, date_sent=dates_sent,
                                       date_paid=dates_paid, amount=amounts, services=services_rendered, paid=paid_bills)
    with engine.connect() as conn:
        conn.execute(stmt)
