from flask import render_template

from app import app
from auth import login_manager, current_user
from models import User

@app.route('/')
def index():
    return render_template('index.htm')
