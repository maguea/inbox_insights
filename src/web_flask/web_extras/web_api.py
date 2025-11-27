# tolu kolade
from flask import request, session, abort, jsonify
import json

from . import api_bp
from src.lib import EMAIL_CONST
from src.lib.email.email_actions import _email_login, _email_save_key, _email_get_by_eid, _email_get_by_page
from src.lib.account.user_categories import save_categories, load_categories

@api_bp.get('/check_email')
def check_email_account():
    username = session.get('email_user')
    server   = session.get('email_server')

    if not username or not server:
        return jsonify({'ok': False, 'msg': 'No email credentials in session'}), 400

    result = _email_login(username, server)
    if result == EMAIL_CONST.LOGIN_SUCCESS:
        return jsonify({'ok': True})
    else:
        return jsonify({'ok': False})

@api_bp.post('/register')
def add_email():
# Get form data
    username = request.form.get('user')
    key = request.form.get('key')
    server = request.form.get('server')
    print(username + ", " + key + ", " + server)

    result = _email_login(user=username, key=key, server=server)
    if result == EMAIL_CONST.IMAP_CONN_FAIL:
        print("STATUS: failed to check IMAP to add_email()")
        return jsonify({'ok': False})
    
    # _user_create_account(username, "") # TODO: remove later. user creation should be done elsewhere
    _email_save_key(username, key)

    # save to session
    session['email_user'] = username
    session['email_server'] = server

    return jsonify({'ok': True})

# List endpoint
@api_bp.get('/emails')
def list_emails():
    username = session.get("email_user")
    if not username:
        abort(401)

    # get the first page (or increase per_page if this is not used for infinite scroll)
    page = request.args.get("page", default=1, type=int)
    if page < 1:
        page = 1
    emails = _email_get_by_page(username, page)

    return jsonify(emails)

# Detail endpoint
@api_bp.get('/emails/<int:eid>')
def get_email(eid: int):
    username = session.get("email_user")
    email = _email_get_by_eid(username, eid)

    if not email:
        abort(404)
    return jsonify(email)

@api_bp.get("/categories")
def categories_list():
    """Return all categories from .env as JSON."""
    username = session.get('email_user')
    return jsonify(load_categories(user=username))

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