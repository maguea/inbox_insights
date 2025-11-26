# tolu kolade
import os
from dotenv import load_dotenv
from math import ceil
import json

from src.lib.email_scraper.email_scraper import Gather

PER_PAGE = 20

def paginate(items, page, per_page=PER_PAGE):
    total = len(items)
    pages = max(1, ceil(total / per_page))
    if page < 1 or page > pages:
        return [], page, pages
    start = (page - 1) * per_page
    end = start + per_page
    return items[start:end], page, pages

def fetch_and_store_emails():
    try:
        current_user = get_current_user()
        if not current_user:
            return None
            
        gatherer = Gather(
            current_user['username'], 
            current_user['password'],
            os.getenv('CLIENT_SERVER', 'imap.gmail.com')
        )
        emails = gatherer._fetch_unread_and_mark_seen()  # Already in correct format!
        
        with open('cached_emails.json', 'w') as f:
            json.dump(emails, f)
            
        return emails
    except Exception as e:
        print(f"Error: {e}")
        return None