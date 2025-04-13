#!/usr/bin/python3
import sys
import os

# Projekt- und venv-Pfad
sys.path.insert(0, '/var/www/hochzeit')
sys.path.insert(0, '/var/www/hochzeit/venv/lib/python3.11/site-packages')

from app import app as application  # Wichtig: "app" muss dein Flask-Objekt sein!
