# tolu kolade
from flask import Blueprint, request, abort, jsonify
import os, json

from src.lib.account.create_accounts import _create_account, _login, _check_env
from src.lib.account.categories import save_categories, load_categories
from src.web_flask.web_extras.testing_extra import SAMPLE_EMAILS
from src.web_flask.web_extras.web_functions_temp import get_error_message, get_current_user

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.get('/valid_email')
def check_email_account():
    user = get_current_user()
    result = _login(user=user['username'],password=user['password'])
    
    return jsonify({'msg': get_error_message(result)})

@api_bp.post('/register')
def add_email():
# Get form data
    username = request.form.get('username')
    password = request.form.get('password')
    server = request.form.get('server')
    _create_account(username, password, server)
    result = _login(username, password)

    return jsonify({'msg': get_error_message(result)})

# List endpoint
@api_bp.get('/emails')
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
@api_bp.get('/emails/<int:eid>')
def get_email(eid: int):
    if os.path.exists('cached_emails.json'):
        with open('cached_emails.json', 'r') as f:
            emails = json.load(f)
    else:
        emails = SAMPLE_EMAILS

    for e in SAMPLE_EMAILS:
        if e["id"] == eid:
            return jsonify(e)
    abort(404)

@api_bp.get("/categories")
def categories_list():
    """Return all categories from .env as JSON."""
    return jsonify(load_categories())

@api_bp.post("/categories")
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
        cats.api_bpend({
            "name": name,
            "emails": emails,
            "domains": domains,
            "shared": shared,
            "days_until_delete": days,
        })

    save_categories(cats)
    return jsonify({"ok": True})

@api_bp.delete("/categories/<name>")
def categories_delete(name):
    """Delete a category by exact name."""
    cats = load_categories()
    new_cats = [c for c in cats if c.get("name") != name]
    deleted = (len(new_cats) != len(cats))
    if deleted:
        save_categories(new_cats)
    return jsonify({"deleted": deleted})