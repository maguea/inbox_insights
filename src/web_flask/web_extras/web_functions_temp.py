# tolu kolade
import os
from dotenv import load_dotenv
from math import ceil
from src.web_flask.web_extras.testing_extra import SAMPLE_EMAILS
from src.lib.email_scraper.email_scraper import Gather

def get_error_message(result_code):
    error_messages = {
        0: 'Success',
        1: "Incorrect email or password",
        2: "Account not set up properly",
        3: "Cannot connect to IMAP server"
    }
    return error_messages.get(result_code, "Unknown error occurred")

def get_current_user():
    try:
        load_dotenv()
        return {
            'username': os.getenv('CLIENT_USER'),
            'password': os.getenv('CLIENT_PASS')
        }
    except:
        return None

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