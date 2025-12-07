# tolu kolade
from flask import request, session, abort, jsonify
import json

from . import api_bp
from src.lib import EMAIL_CONST
from src.lib.email.email_actions import _email_login, _email_save_key, _email_get_by_eid, _email_get_by_page
from src.lib.email.email_move2_db import _email_move_to_database
from src.lib.account.user_categories import save_categories, load_categories
from src.lib.account.user_accounts import _user_login


@api_bp.post('/check_user')
def check_user_account():
    username = request.form.get('user')
    password = request.form.get('pass')
    server = request.form.get('server')
    if not username or not password or not server:
        return jsonify({'ok': False, 'msg': 'missing credentials'}), 400

    res = _user_login(username, password)
    if res == EMAIL_CONST.IMAP_CONN_FAIL:
        return jsonify({'ok': False, 'msg': 'invalid credentials'}), 401

    return jsonify({'ok': True, 'msg': 'user exists'})


@api_bp.get('/check_email_account')
def check_email_account():
    username = session.get('email_user')
    server = session.get('email_server')
    if not username or not server:
        return jsonify({'ok': False, 'msg': 'Not connected'})

    # Use db-based check (does a key exist / is it valid?)
    res = _email_login(user=username, server=server)
    if res == EMAIL_CONST.IMAP_CONN_FAIL:
        return jsonify({'ok': False, 'msg': 'Not connected'})
    return jsonify({'ok': True, 'msg': 'Connected to email server'})


@api_bp.post('/login')
def email_login():
    username = request.form.get('user')
    server = request.form.get('server')
    key = request.form.get('key')

    if not username or not server or not key:
        return jsonify({'ok': False, 'msg': 'Missing user/server/key'}), 400

    res = _email_login(username, server, key)
    if res == EMAIL_CONST.IMAP_CONN_FAIL:
        return jsonify({'ok': False, 'msg': 'Email login failed'}), 401

    session['email_user'] = username
    session['email_server'] = server
    return jsonify({'ok': True, 'msg': 'Email login successful'})


@api_bp.post('/save_key')
def save_key():
    username = request.form.get('user')
    server = request.form.get('server')
    key = request.form.get('key')
    if not username or not server or not key:
        return jsonify({'ok': False, 'msg': 'Missing user/server/key'}), 400

    res = _email_save_key(username, server, key)
    if res == EMAIL_CONST.IMAP_CONN_FAIL:
        return jsonify({'ok': False, 'msg': 'Email login failed'}), 401

    session['email_user'] = username
    session['email_server'] = server

    return jsonify({'ok': True, 'msg': 'Key saved and login verified'})


@api_bp.post('/update_emails')
def update_emails():
    username = session.get('email_user')
    server = session.get('email_server')
    if not username or not server:
        return jsonify({"ok": False, "msg": "No logged in email user"}), 401

    try:
        result = _email_move_to_database(username, server)
        if result == EMAIL_CONST.IMAP_CONN_FAIL:
            return jsonify({"ok": False, "msg": "Failed to connect to IMAP"}), 502
        elif result == EMAIL_CONST.NO_EMAILS:
            return jsonify({"ok": True, "msg": "No new emails to import"})
    except Exception as exc:
        print("ERROR: update_emails failed:", repr(exc))
        return jsonify({"ok": False, "msg": "Failed to update emails"}), 500

    return jsonify({"ok": True, "msg": "Emails updated successfully"})


@api_bp.get("/categories")
def categories_list():
    """Return all categories as JSON."""
    username = session.get('email_user')
    if not username:
        return jsonify({"ok": False, "msg": "No logged in email user"}), 401

    raw_categories = load_categories(user=username) or []
    categories = []
    for cat in raw_categories:
        if not isinstance(cat, dict):
            continue
        if not cat.get("color"):
            cat["color"] = "#4a90e2"
        categories.append(cat)

    return jsonify({"ok": True, "categories": categories})


@api_bp.post("/categories")
def categories_upsert():
    """
    Create/update a category.
    Accepts JSON or form-encoded fields:
      name (str, required)
      emails/domains (list[str] OR comma-separated str)
      days_until_delete (int)
      color (hex string, optional; defaults to #4a90e2)
    """
    username = session.get("email_user")
    if not username:
        return jsonify({"ok": False, "msg": "No logged in email user"}), 401

    data = request.get_json(silent=True) or request.form
    name = (data.get("name") or "").strip()
    if not name:
        return jsonify({"ok": False, "msg": "Category name is required"}), 400

    # emails/domains can come in a few shapes
    raw_emails = (
        data.get("emails")
        or data.get("domains")
        or data.get("emails_domains")
    )

    if isinstance(raw_emails, str):
        emails = [e.strip() for e in raw_emails.split(",") if e.strip()]
    elif isinstance(raw_emails, list):
        emails = [str(e).strip() for e in raw_emails if str(e).strip()]
    else:
        emails = []

    days = data.get("days_until_delete", None)
    try:
        days_until_delete = int(days) if days not in (None, "",) else None
    except ValueError:
        return jsonify({"ok": False, "msg": "days_until_delete must be an integer"}), 400

    color = data.get("color") or "#4a90e2"

    # Load existing categories from PG
    categories = load_categories(user=username) or []

    # Upsert logic
    updated = False
    for cat in categories:
        if cat.get("name") == name:
            cat["emails"] = emails
            cat["days_until_delete"] = days_until_delete
            cat["color"] = color
            updated = True
            break

    if not updated:
        categories.append({
            "name": name,
            "emails": emails,
            "days_until_delete": days_until_delete,
            "color": color,
        })

    # Save back to PG
    save_categories(user=username, categories=categories)

    return jsonify({
        "ok": True,
        "category": {
            "name": name,
            "emails": emails,
            "days_until_delete": days_until_delete,
            "color": color,
        }
    })


@api_bp.delete("/categories/<name>")
def categories_delete(name):
    """Delete a category by exact name."""
    username = session.get("email_user")
    if not username:
        return jsonify({"ok": False, "msg": "No logged in email user"}), 401

    name = name.strip()
    categories = load_categories(user=username) or []
    new_categories = [c for c in categories if c.get("name") != name]

    if len(new_categories) == len(categories):
        return jsonify({"ok": False, "msg": "Category not found"}), 404

    save_categories(user=username, categories=new_categories)
    return jsonify({"ok": True})


@api_bp.get('/emails')
def list_emails():
    username = session.get("email_user")
    if not username:
        abort(401)

    category = request.args.get('cat', None)
    page = request.args.get("page", default=1, type=int)
    if page < 1:
        page = 1
        
    emails = _email_get_by_page(user=username, page=page, cat=category)

    return jsonify(emails)


@api_bp.get('/emails/<int:eid>')
def get_email(eid: int):
    username = session.get("email_user")
    email = _email_get_by_eid(username, eid)

    if not email:
        abort(404)

    # Could transform more fields if desired
    return jsonify(email)


@api_bp.post('/register')
def add_email():
    '''
    register a new user or email session'''
    username = request.form.get('user')
    key = request.form.get('key')
    server = request.form.get('server')
    # print(username + ", " + key + ", " + server)

    result = _email_login(user=username, key=key, server=server)
    if result == EMAIL_CONST.IMAP_CONN_FAIL:
        print("STATUS: failed to check IMAP to add_email()")
        return jsonify({'ok': False, 'msg': 'IMAP connection failed'})

    print("STATUS: IMAP connection success")

    _email_save_key(user=username, server=server, key=key)

    session['email_user'] = username
    session['email_server'] = server

    return jsonify({'ok': True})
