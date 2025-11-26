# tolu kolade
from flask import request, abort, jsonify
from . import api_bp

from src.lib.account.create_accounts import _create_account, _login
from src.lib.account.categories import save_categories, load_categories
from src.lib import EMAIL_CONST, get_error_message


@api_bp.post('/check_email')
def check_email_account():
    username = request.form.get('user')
    password = request.form.get('pass')
    server = request.form.get('server')

    result = _login(username, password, server)
    if result == EMAIL_CONST.LOGIN_SUCCESS:
        return jsonify({'ok': True})
    else:
        return jsonify({'ok': False})

@api_bp.post('/register')
def add_email():
# Get form data
    username = request.form.get('user')
    password = request.form.get('pass')
    server = request.form.get('server')

    result = _login(username, password, server)
    if result == EMAIL_CONST.IMAP_CONN_FAIL:
        return jsonify({'ok': False})
    
    _create_account(username, password, server)
    return jsonify({'ok': True})

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
    } for e in emails])

# Detail endpoint
@api_bp.get('/emails/<int:eid>')
def get_email(eid: int):

    for e in emails:
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