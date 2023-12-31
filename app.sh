#!/bin/bash
source venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:${PWD}"
export HOST="0.0.0.0"
export PORT=8000
export FLASK_DEBUG=1
export FLASK_APP=src/app.py
flask run --host=$HOST --port=$PORT