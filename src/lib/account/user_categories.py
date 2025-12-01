# src/lib/account/user_categories.py
import json
from src.lib.database.db_actions import DB_Actions


def save_categories(user, categories, password: str = ""):
    """
    Save a list of categories (as dicts) into db.

    Example category dict:
      {
        "name": "Work",
        "emails": ["boss@corp.com"],
        "domains": ["corp.com"],
        "shared": false,
        "days_until_delete": 30
      }
    """
    db = DB_Actions()
    categories_json = json.dumps(categories)
    # priv_cats is stored as JSONB in public.user_data
    return db._add_categories((user, password,), categories_json)


def load_categories(user, password: str = ""):
    """
    Load categories list from server.

    Returns a Python list of category dicts, or [] if nothing stored.
    """
    db = DB_Actions()
    raw = db._gather_categories((user, password,))

    if not raw:
        return []

    # psycopg2 may already decode JSONB into Python objects
    if isinstance(raw, (list, dict)):
        return raw

    # If it's a string, parse JSON
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except Exception:
            return []

    # Fallback
    return []
