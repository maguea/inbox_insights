# src/lib/account/categories.py
import json
from src.lib.database.db_actions import DB_Actions

def save_categories(user, categories, password=""):
    """
    Save a list of categories (as dicts) into db.
    Example category dict:
      {
        "name": "Work",
        "emails": ["boss@corp.com"],
        "days_until_delete": 30
      }
    """
    # TODO: implement

    # save category
    db = DB_Actions()
    categories_json = json.dumps(categories)
    return db._add_categories((user, password,), categories_json)

def load_categories(user, password=""):
    """
    Load categories list from server.
    """
    db = DB_Actions()
    return db._gather_categories((user, password,))

def apply_categories():
    # should apply categories to emails
    return None