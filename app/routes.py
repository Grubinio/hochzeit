# app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.db import get_db_connection

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


@main.route('/antwort', methods=['GET', 'POST'])
def antwort():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        zusage = request.form['zusage']
        nachricht = request.form.get('nachricht', '')

        #conn = get_db_connection()
        #cursor = conn.cursor()
        #cursor.execute("""
        #    INSERT INTO antworten (name, email, zusage, nachricht)
        #    VALUES (%s, %s, %s, %s)
        #""", (name, email, zusage, nachricht))
        #conn.commit()
        #cursor.close()
        #conn.close()

        flash("Danke für deine Antwort!", "success")
        return redirect(url_for('antwort'))

    return render_template('zusage.html')