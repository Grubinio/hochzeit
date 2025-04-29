import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv('/var/www/hochzeit/.env')  # Pfad ggf. anpassen

try:
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    cursor = conn.cursor()
    cursor.execute("SELECT name, email FROM rueckmeldungen LIMIT 3")
    for row in cursor.fetchall():
        print(row)
    cursor.close()
    conn.close()
except Exception as e:
    print("❌ DB-Fehler:", e)
