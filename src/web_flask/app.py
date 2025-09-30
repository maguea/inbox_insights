# tolu kolade
from flask import Flask, render_template, request, redirect
# from pathlib import Path
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.account.create_accounts import _create_account, _login

app = Flask(__name__)

@app.route('/')
def index():
    # TODO: temp. MUST REMOVE
    _create_account('insighti338@gmail.com', 'Y<0;y4T3R>@&', 'imap.google.com')
    result = _login('insighti338@gmail.com', 'Y<0;y4T3R>@&')
    # TODO: check if user already has an account
    if False:
        return redirect(url_for('login'))
    return render_template('dashboard.html', code=result)

@app.route('/config', methods=['GET', 'POST'])
def client_settings():
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        password = request.form.get('password')
        server = request.form.get('server')


        _create_account(username, password, server)
        result = _login(username, password) # ideally use this to show status

        
        # Redirect or render with success message
        return render_template('settings.html', success=True, code=result)
    
    return render_template('settings.html')

@app.route('/history')
def view_all_emails():
    return render_template('history.html')


if __name__ == '__main__':
    app.run(port=6222, debug=True)