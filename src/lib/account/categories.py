# src/lib/account/categories.py
import os, json
from pathlib import Path
from dotenv import set_key, load_dotenv

ENV_PATH = Path(".env")
ENV_KEY = "CATEGORIES"

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
    set_key(str(ENV_PATH), ENV_KEY, json.dumps(categories))

def load_categories() -> list[dict]:
    """
    Load categories list from .env. Returns [] if not found.
    """
    load_dotenv()
    raw = os.getenv(ENV_KEY)
    if not raw:
        return []
    try:
        return json.loads(raw)
    except:
        return []
