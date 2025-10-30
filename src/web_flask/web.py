# tolu kolade
from flask import Flask, render_template, redirect, url_for
import os, json

from src.lib.account.create_accounts import _check_env
from src.web_flask.web_extras.web_functions_temp import get_current_user, paginate, fetch_and_store_emails
from src.web_flask.web_extras.web_api import api_bp
from src.web_flask.web_extras.testing_extra import SAMPLE_EMAILS

app = Flask(__name__)
app.register_blueprint(api_bp)

@app.route('/')
def index():
    result = _check_env()
    if result == False:
        return redirect(url_for('client_settings'))
    
    if not os.path.exists('cached_emails.json'):
        fetch_and_store_emails()
    
    return render_template('dashboard.html')

@app.route('/config')
def client_settings():
    # Check if .env file exists
    user = get_current_user()

    return render_template('settings.html', user=user)


@app.route('/history')
def view_all_emails():
    if os.path.exists('cached_emails.json'):
        with open('cached_emails.json', 'r') as f:
            emails = json.load(f)
    else:
        # Fallback to sample emails if no cache exists
        emails = SAMPLE_EMAILS
    return render_template('history.html', emails=emails)


@app.get("/history/page/<int:page>")
def history_page(page):
    emails, page, pages = paginate(SAMPLE_EMAILS, page)
    # If page is out of range, return 204 (no content) so the scroller stops.
    if not emails and page > 1:
        return ("", 204)
    # Return only the batch items HTML (Jinja fragment)
    return render_template(
        "partials/email_items.html",
        emails=emails
    )
