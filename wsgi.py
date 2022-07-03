from app import create_app
from flask import render_template, redirect
from datetime import datetime
import pytz, requests as req

app = create_app()



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)