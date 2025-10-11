# tolu kolade
from app import Flask, render_template, request, redirect
# from pathlib import Path
import sys
import os
from app import Flask, request, jsonify, render_template
from src.lib.account.categories import save_categories, load_categories



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.lib.account.create_accounts import _create_account, _login

app = Flask(__name__)

@app.route('/')
def index():
    result = _login()
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