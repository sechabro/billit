from app import app
from flask import render_template
from app.models import InvoiceModel

@app.route('/dashboard')
def index():
    return render_template('admin/dashboard.html')