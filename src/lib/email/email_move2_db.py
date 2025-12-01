import json
from datetime import timedelta
from datetime import datetime as dt
from datetime import timezone as tz


from src.lib.account.user_categories import load_categories
from src.lib.database.db_actions import DB_Actions
from src.lib.email.email_scraper import Gather

DEFAULT_DAYS_UNTIL_DELETE = 30

def _email_move_to_database(user, server, key=None):
    '''
    Calls the Gather class to get new emails and moves them to the DB.

    :param user:   username / email (stored into user_id column)
    :param server: IMAP server hostname
    :param key:    email password (if None, pulled from DB)
    '''
    db = DB_Actions()

    # Get password if not provided
    if key is None:
        # TODO: update logic for additional users
        key = db._gather_user_key((user, "",))

    # Load category rules from categories file
    categories = load_categories(user=user)  # list of dicts with name/emails/days_until_delete

    # Fetch unread emails from IMAP
    gather = Gather(user, key, server)
    emails = gather._fetch_unread_and_mark_seen()

    now = dt.now(tz.utc)
    db._delete_old_emails()

    for email_obj in emails:
        sender_info = email_obj.get("sender", {}) or {}
        sender_addr = (sender_info.get("address") or "").strip()
        sender_name = (sender_info.get("name") or "").strip()

        # Default category/delete_date
        category_name = db._get_cat_by_sender(sender_addr)
        delete_date = None

        # If no category matched, still default to 30 days
        if delete_date is None:
            delete_date = now + timedelta(days=DEFAULT_DAYS_UNTIL_DELETE)

        # Build the `data` JSON for the DB
        data_payload = {
            "subject": email_obj["subject"],
            "preview": email_obj["preview"],
            "data": email_obj["body"],
        }
        data_json = json.dumps(data_payload)
        # build the sender info for the db
        sender_payload = {
            "sender_name": sender_name,
            "sender_addr": sender_addr
        }
        sender_json = json.dumps(sender_payload)

        # Row layout: (user_id, sender_add, category, data, delete_date)
        row = (
            user,               # user_id
            sender_json,        # sender_add 
            category_name,      # category (or None)
            data_json,          # data (text/JSON)
            delete_date,         # delete_date (timestamp or None)
        )
        db._add_email_data(row)
