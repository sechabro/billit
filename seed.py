import imp
from faker import Faker
from flask import jsonify
import requests
from datetime import datetime
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker, declarative_base
from app.api.clients import ClientModel

fake = Faker()

engine = create_engine('postgresql://postgres@localhost:5432/billit')
Session = sessionmaker(bind=engine)
Base = declarative_base()


invoices = 400

'''companies = 100
for i in range(companies):
    company_name = fake.company()
    contact_name = fake.name()
    addresses = fake.street_address()
    cities = fake.city()
    states = fake.random_elements(elements=('AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY'), length=1, unique=False)
    zipcodes = fake.postcode()
    stmt = insert(ClientModel).values(company=company_name, contact=contact_name, address=addresses, city=cities, state=states, zipcode=zipcodes)
    with engine.connect() as conn:
        conn.execute(stmt)'''