from app import app
from flask import render_template

@app.route('/')
def index_home():
    return render_template('public/index.html')