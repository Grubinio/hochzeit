#!/usr/bin/python3
import sys
import os

# Aktivieren des virtualenv-Umfelds (wenn nötig)
# sys.path.insert(0, '/var/www/hochzeit/venv/bin')  # optional

# Projektverzeichnis & site-packages hinzufügen
sys.path.insert(0, '/var/www/hochzeit')
sys.path.insert(0, '/var/www/hochzeit/venv/lib/python3.11/site-packages')

# Umgebungsvariable setzen (optional, falls nötig)
os.environ['FLASK_ENV'] = 'production'

# App aus Factory laden
from app import create_app
application = create_app()
