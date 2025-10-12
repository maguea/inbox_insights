# tolu kolade
from flask import Flask, render_template, request, redirect, url_for, abort
from flask import jsonify, render_template

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.account.create_accounts import _create_account, _login, _check_env
from lib.account.categories import save_categories, load_categories
from testing_extra import SAMPLE_EMAILS

app = Flask(__name__)

@app.route('/')
def index():
    result = _check_env()
    # TODO: check if user already has an account
    if result == False:
        return redirect(url_for('client_settings'))
    

    return render_template('dashboard.html')

@app.route('/config', methods=['GET', 'POST'])
def client_settings():
    # Check if .env file exists
    env_exists = os.path.exists('.env')
    connection_status = None
    success = False
    error = None
    
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        password = request.form.get('password')
        server = request.form.get('server')

        try:
            if not env_exists:
                # First time setup - create account
                _create_account(username, password, server)
                result = _login(username, password)
                
                if result == 0:
                    success = True
                    connection_status = "success"
                else:
                    error = get_error_message(result)
                    
            else:
                # .env exists - test connection with new credentials
                result = _login(username, password)
                
                if result == 0:
                    success = True
                    connection_status = "success"
                    # Update credentials in .env or database
                    _create_account(username, password, server)
                else:
                    error = get_error_message(result)
                    
        except Exception as e:
            error = f"Unexpected error: {str(e)}"
    
    # If .env exists and it's a GET request, test current connection
    current_status = None
    if env_exists and request.method == 'GET':
        # You might want to get current credentials from .env
        current_user = get_current_user()  # You'll need to implement this
        if current_user:
            result = _login(current_user['username'], current_user['password'])
            current_status = {
                'status': 'success' if result == 0 else 'error',
                'message': get_error_message(result) if result != 0 else "Successfully connected to email server",
                'email': current_user['username']
            }
    
    return render_template(
        'settings.html',
        env_exists=env_exists,
        success=success,
        error=error,
        connection_status=connection_status,
        current_status=current_status
    )

def get_error_message(result_code):
    error_messages = {
        1: "Incorrect email or password",
        2: "Account not set up properly",
        3: "Cannot connect to IMAP server"
    }
    return error_messages.get(result_code, "Unknown error occurred")

def get_current_user():
    try:
        from dotenv import load_dotenv
        load_dotenv()
        return {
            'username': os.getenv('CLIENT_USER'),
            'password': os.getenv('CLIENT_PASS')
        }
    except:
        return None

@app.route('/history')
def view_all_emails():
    return render_template('history.html', emails=SAMPLE_EMAILS)

# List endpoint
@app.get('/api/emails')
def list_emails():
    return jsonify([{
        "id": e["id"],
        "sender": e["sender"],
        "subject": e["subject"],
        "preview": e["preview"],
        "timestamp": e["timestamp"],
        "date": e["date"]
    } for e in SAMPLE_EMAILS])

# Detail endpoint
@app.get('/api/emails/<int:eid>')
def get_email(eid: int):
    for e in SAMPLE_EMAILS:
        if e["id"] == eid:
            return jsonify(e)
    abort(404)


@app.get("/categories")
def categories_list():
    """Return all categories from .env as JSON."""
    return jsonify(load_categories())

@app.post("/categories")
def categories_upsert():
    """
    Create/update a category.
    Accepts JSON or form-encoded fields:
      name (str, required)
      emails (list[str] OR comma-separated str)
      domains (list[str] OR comma-separated str)
      shared (bool OR 'on'/'true'/'1')
      days_until_delete (int)
    """
    data = request.get_json(silent=True) or request.form.to_dict(flat=True) or {}

    name = data.get("name", "").strip()
    if not name:
        return jsonify({"ok": False, "error": "name is required"}), 400

    # allow list or comma-separated strings
    def coerce_list(v):
        if isinstance(v, list): 
            return v
        if isinstance(v, str):
            return [x.strip() for x in v.split(",") if x.strip()]
        return []

    emails  = coerce_list(data.get("emails", []))
    domains = coerce_list(data.get("domains", []))

    # accept bools/ints
    shared_raw = data.get("shared", False)
    if isinstance(shared_raw, str):
        shared = shared_raw.lower() in ("true", "1")
    else:
        shared = bool(shared_raw)

    try:
        days = int(data.get("days_until_delete", 0))
    except Exception:
        return jsonify({"ok": False, "error": "days_until_delete must be int"}), 400

    cats = load_categories()

    # Upsert by exact name
    replaced = False
    for i, c in enumerate(cats):
        if c.get("name") == name:
            cats[i] = {
                "name": name,
                "emails": emails,
                "domains": domains,
                "shared": shared,
                "days_until_delete": days,
            }
            replaced = True
            break

    if not replaced:
        cats.append({
            "name": name,
            "emails": emails,
            "domains": domains,
            "shared": shared,
            "days_until_delete": days,
        })

    save_categories(cats)
    return jsonify({"ok": True})

@app.delete("/categories/<name>")
def categories_delete(name):
    """Delete a category by exact name."""
    cats = load_categories()
    new_cats = [c for c in cats if c.get("name") != name]
    deleted = (len(new_cats) != len(cats))
    if deleted:
        save_categories(new_cats)
    return jsonify({"deleted": deleted})


if __name__ == '__main__':
    app.run(port=6222, debug=True)

