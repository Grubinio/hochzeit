from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

from dotenv import load_dotenv
#dotenv_path = Path(__file__).resolve().parent / '.env'
load_dotenv('/var/www/hochzeit/.env')

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-key")

# Passwörter aus .env
PW_MEERSBURG = os.getenv("PASSWORD_MEERSBURG")
PW_MAIN = os.getenv("PASSWORD_MAIN")
PW_BOTH = os.getenv("PASSWORD_BOTH")


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        entered_pw = request.form.get('password').strip()

        if entered_pw == PW_MEERSBURG:
            session['access'] = 'meersburg'
            return redirect(url_for('meersburg'))

        elif entered_pw == PW_MAIN:
            session['access'] = 'main'
            return redirect(url_for('main'))

        else:
            flash('Falsches Passwort – bitte erneut versuchen.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/main')
def main():
    if session.get('access') in ['main', 'both']:
        return render_template('main.html')
    return redirect(url_for('login'))

@app.route('/meersburg')
def meersburg():
    if session.get('access') in ['meersburg', 'both']:
        return render_template('meersburg.html')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Nur für lokalen Test
if __name__ == '__main__':
    app.run(debug=True)

@app.route('/antwort', methods=['GET', 'POST'])
def antwort():
    if request.method == 'POST':
        render_template('zusage.html')
        #name = request.form['name']
        #email = request.form['email']
        #zusage = request.form['zusage']
        #nachricht = request.form.get('nachricht', '')
        #flash("Danke für deine Antwort!", "success")
        #return redirect(url_for('main.antwort'))
    return render_template('zusage.html')