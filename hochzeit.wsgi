#!/usr/bin/python3
import sys
import os

# Projekt- und venv-Pfad
sys.path.insert(0, '/var/www/hochzeit')
sys.path.insert(0, '/var/www/hochzeit/venv/lib/python3.11/site-packages')

# App aus Factory laden
from app import create_app
application = create_app()