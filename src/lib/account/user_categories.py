# src/lib/account/categories.py
import json
from src.lib.database.db_actions import DB_Actions

def save_categories(categories: list[dict]):
    """
    Save a list of categories (as dicts) into .env.
    Example category dict:
      {
        "name": "Work",
        "emails": ["boss@corp.com"],
        "domains": ["corp.com"],
        "shared": True,
        "days_until_delete": 30
      }
    """
    # TODO: implement
    set_key(str(ENV_PATH), ENV_KEY, json.dumps(categories))

def load_categories(user, password):
    """
    Load categories list from server.
    """
    db = DB_Actions()
    return db._gather_categories(user, password)
