from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import mysql.connector.pooling

from dotenv import load_dotenv
#dotenv_path = Path(__file__).resolve().parent / '.env'
load_dotenv('/var/www/hochzeit/.env')

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-key")

# Passwörter aus .env
PW_MEERSBURG = os.getenv("PASSWORD_MEERSBURG")
PW_MAIN = os.getenv("PASSWORD_MAIN")
PW_ADMIN = os.getenv("PASSWORD_ADMIN")

# Konfiguration für Sessions
app.config['SESSION_COOKIE_SECURE'] = True          # nur über HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True        # nicht per JS lesbar
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'       # gegen CSRF



# Konfiguration für MySQL-Datenbankverbindung
dbconfig = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

# Erstellen eines Connection Pools
try:
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="hochzeit_pool",
        pool_size=5,
        **dbconfig
    )
except mysql.connector.Error as err:
    print("⚠️ Datenbankverbindung fehlgeschlagen – weiter im Offline-Modus.")
    connection_pool = None


def get_db_connection():
    return connection_pool.get_connection()

#Routen
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
        
        elif entered_pw == PW_ADMIN:
            session['access'] = 'admin'
            return redirect(url_for('admin'))

        else:
            flash('Falsches Passwort – bitte erneut versuchen.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/main')
def main():
    if session.get('access') in ['main']:
        return render_template('main.html')
    return redirect(url_for('login'))

from flask import Response
import csv

from datetime import datetime

@app.route('/admin')
def admin_view():
    if session.get('access') not in ['main', 'both']:
        return redirect(url_for('login'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM rueckmeldungen ORDER BY eingegangen_am DESC")
        rueckmeldungen = cursor.fetchall()
        # Datum formatieren
        for eintrag in rueckmeldungen:
            if isinstance(eintrag["eingegangen_am"], datetime):
                eintrag["eingegangen_am"] = eintrag["eingegangen_am"].strftime('%d.%m.%Y %H:%M')
        cursor.close()
        conn.close()
    except Exception as e:
        print("Fehler beim Laden der Daten:", e)
        flash(f"Fehler beim Laden der Daten: {e}", "danger")
        rueckmeldungen = []

    return render_template('admin.html', daten=rueckmeldungen)



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
    app.run() #debug=True

@app.route('/antwort', methods=['GET', 'POST'])
def antwort():
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        zusage = request.form.get("zusage")
        essen = request.form.get("essen")
        partner_zusage = request.form.get("zusage-p")
        partner_essen = request.form.get("essen-p")
        nachricht = request.form.get("nachricht")
        session_id = session.get("access", None)  # oder "user_id" falls du das speicherst

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO rueckmeldungen 
                (name, email, zusage, essen, partner_zusage, partner_essen, nachricht, session_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (name, email, zusage, essen, partner_zusage, partner_essen, nachricht, session_id))
            conn.commit()
            cursor.close()
            conn.close()
            flash("Danke für deine Antwort 💌", "success")
        except Exception as e:
            print("Fehler beim Einfügen:", e)
            flash("Fehler beim Speichern 😢", "danger")

        return redirect(url_for("main"))

    # GET → zeigt das Formular an
    return render_template("zusage.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', error=e), 500