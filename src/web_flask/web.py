# tolu kolade
from flask import Flask, session, render_template
import os, secrets
from dotenv import load_dotenv, set_key

from src.lib.email.email_move2_db import _email_move_to_database
from src.web_flask.web_extras import api_bp, bp_login
from src.lib import EMAIL_CONST

app = Flask(__name__)

# add secret key for session
load_dotenv()
secret_key = os.getenv('FLASK_SECRET_KEY')
if secret_key == None:
    secret_key = secrets.token_urlsafe(16)
    set_key(".env", 'FLASK_SECRET_KEY', secret_key)
app.secret_key = secret_key

# add blueprints
app.register_blueprint(api_bp)
app.register_blueprint(bp_login)

@app.route('/')
def index():
    username = session.get('email_user')
    server   = session.get('email_server')

    _email_move_to_database(user=username, server=server)
    return render_template('dashboard.html')

@app.route('/config')
def client_settings():
    user = EMAIL_CONST.GMAIL['user']
    return render_template('settings.html', user=user)

@app.route('/history')
def view_all_emails():
    return render_template('history.html')
