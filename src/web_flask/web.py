# tolu kolade
from flask import Flask, render_template, request, redirect, url_for

from src.lib.account.create_accounts import _create_account, _login, _check_env
from src.web_flask.web_extras.web_functions_temp import get_error_message, get_current_user
from src.web_flask.web_extras.web_api import api_bp

app = Flask(__name__)
app.register_blueprint(api_bp)

@app.route('/')
def index():
    result = _check_env()
    # TODO: check if user already has an account
    if result == False:
        return redirect(url_for('client_settings'))
    
    return render_template('dashboard.html')

@app.route('/config')
def client_settings():
    # Check if .env file exists
    user = get_current_user()

    return render_template('settings.html', user=user)


@app.route('/history')
def view_all_emails():
    return render_template('history.html')