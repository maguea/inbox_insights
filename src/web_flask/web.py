# tolu kolade
from flask import Flask, render_template
import os, secrets
from dotenv import load_dotenv, set_key

from src.web_flask.web_extras import api_bp, bp_login
from src.lib import EMAIL_CONST

app = Flask(__name__)

load_dotenv()
secret_key = os.getenv('FLASK_SECRET_KEY')
if secret_key == None:
    secret_key = secrets.token_urlsafe(16)
    set_key(".env", 'FLASK_SECRET_KEY', secret_key)
app.secret_key = secret_key

app.register_blueprint(api_bp)
app.register_blueprint(bp_login)

@app.route('/')
def index():    
    return render_template('dashboard.html')

@app.route('/config')
def client_settings():
    user = EMAIL_CONST.GMAIL['user']
    return render_template('settings.html', user=user)

@app.route('/history')
def view_all_emails():
    return render_template('history.html')
