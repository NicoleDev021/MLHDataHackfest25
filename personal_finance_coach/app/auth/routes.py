from flask import Blueprint, render_template, redirect, url_for
from app.auth.decorators import login_required

auth = Blueprint('auth', __name__)

@auth.route('/')
@auth.route('/login')
def login():
    return render_template('auth/login.html')

@auth.route('/dashboard')
@login_required
def dashboard():
    return render_template('auth/dashboard.html')