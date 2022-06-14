from app import app
from flask import render_template

@app.route('/dashboard')
def index():
    return render_template('admin/admin_template.html')