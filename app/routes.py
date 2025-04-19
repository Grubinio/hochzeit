# app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

import logging
logging.basicConfig(level=logging.DEBUG)


main = Blueprint('main', __name__)

# Dummy-Login-Daten (kannst du später anpassen oder mit DB verbinden)
USERNAME = 'gast'
PASSWORD = 'liebe'

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == USERNAME and password == PASSWORD:
            session['user'] = username
            return redirect(url_for('main.home'))
        else:
            flash("Falsche Zugangsdaten!")
    return render_template('login.html')

@main.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('main.login'))
    return render_template('main.html')

@main.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('main.login'))

