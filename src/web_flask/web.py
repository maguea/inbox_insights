# tolu kolade
from flask import (
    Flask,
    redirect,
    session,
    render_template,
    url_for,
    jsonify,
    request,
)
import os, secrets
from dotenv import load_dotenv, set_key

from src.web_flask.web_extras import api_bp, bp_login
from src.lib import EMAIL_CONST, DB_CONST
from src.lib.account.user_categories import load_categories, save_categories
from src.lib.email import email_actions
from src.lib.database.db_actions import DB_Actions

app = Flask(__name__)

# add secret key for session
load_dotenv()
secret_key = os.getenv("FLASK_SECRET_KEY")
if secret_key is None:
    secret_key = secrets.token_urlsafe(16)
    set_key(".env", "FLASK_SECRET_KEY", secret_key)
app.secret_key = secret_key

# add blueprints
app.register_blueprint(api_bp)
app.register_blueprint(bp_login)


@app.route("/")
def index():
    username = session.get("email_user")
    server = session.get("email_server")
    if not username and not server:
        return redirect(url_for("client_login"))
    # pass username for convenience in template
    return render_template("dashboard.html", user=username)


@app.route("/config")
def client_settings():
    user = session.get("email_user")
    return render_template("settings.html", user=user)


@app.route("/login")
def client_login():
    return render_template("login_page.html")


@app.route("/history")
def view_all_emails():
    return render_template("history.html")


@app.before_request
def make_session_permanent():
    session.permanent = True


# ---------- JSON API: categories ----------

@app.route("/api/categories", methods=["GET", "POST"])
def api_categories():
    """
    GET  -> return current user's categories
    POST -> replace current user's categories
    """
    user = session.get("email_user")
    if not user:
        return jsonify({"error": "not logged in"}), 401

    if request.method == "GET":
        cats = load_categories(user=user) or []
        return jsonify({"categories": cats})

    # POST
    payload = request.get_json(silent=True) or {}
    cats = payload.get("categories", [])
    # basic safety: ensure it's a list
    if not isinstance(cats, list):
        return jsonify({"error": "categories must be a list"}), 400

    save_categories(user=user, categories=cats)
    return jsonify({"status": "ok"})


# ---------- JSON API: emails (sorted + deletable) ----------

@app.route("/api/emails", methods=["GET"])
def api_emails():
    """
    List paged emails for the logged in user.

    Query params:
      page     (int, default 1)
      category (string; 'all' or specific category)
    """
    user = session.get("email_user")
    if not user:
        return jsonify({"error": "not logged in"}), 401

    try:
        page = int(request.args.get("page", "1"))
    except ValueError:
        page = 1
    if page < 1:
        page = 1

    category = request.args.get("category", "all")
    emails = email_actions._email_get_by_page(user, page, category)

    return jsonify({"page": page, "category": category, "emails": emails})


@app.route("/api/email/<int:email_id>", methods=["GET", "DELETE"])
def api_email_detail(email_id: int):
    """
    GET    -> full email details
    DELETE -> delete this email from DB for current user
    """
    user = session.get("email_user")
    if not user:
        return jsonify({"error": "not logged in"}), 401

    if request.method == "GET":
        email_obj = email_actions._email_get_by_eid(user, email_id)
        if not email_obj:
            return jsonify({"error": "not found"}), 404
        return jsonify(email_obj)

    # DELETE
    db = DB_Actions()
    result = db._delete_email(user, email_id)
    if result == DB_CONST.DB_ERROR:
        return jsonify({"status": "error"}), 500
    return jsonify({"status": "deleted"})
