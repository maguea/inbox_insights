# web.py Tolu Kolade Sept 29, 2025
# This is the main entry point for the web app. 
# it creates the flask app and defines the root webpages and 
# adds blueprints for supplemental pages
# 

from flask import Flask, redirect, session, render_template, url_for
import os, secrets
from dotenv import load_dotenv, set_key

from src.web_flask.web_extras import api_bp, bp_login
from src.lib.email.email_actions import _email_get_dashboard

app = Flask(__name__)

# add secret key for sessions
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
    '''
    will redirect to login page if no session
    '''
    username = session.get('email_user')
    server   = session.get('email_server')
    if not username or not server:
        return redirect(url_for('login.login_page'))
    
    # Fetch 3 newest emails per category
    sections = _email_get_dashboard(username, per_category=3)

    return render_template(
        'dashboard.html',
        sections=sections,
        user=username
    )

@app.route('/config')
def client_settings():
    user = session.get('email_user')
    return render_template('settings.html', user=user)


@app.route('/history')
def view_all_emails():
    return render_template('history.html')

@app.before_request
def make_session_permanent():
    '''
    makes the session be permanent
    '''
    session.permanent = True
