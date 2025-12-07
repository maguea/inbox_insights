import json

from src.lib import EMAIL_CONST
from src.lib.database.db_actions import DB_Actions
from src.lib.email.email_scraper import Gather


def _to_iso(val):
    """Convert datetime/date values to iso strings for JSON."""
    if val is None:
        return None
    try:
        return val.isoformat()
    except Exception:
        return str(val)


def _email_login(user, server, key=None):
    """
    Checks basic connection.
        Returns:
        - 0: Success
        - 3: IMAP server connection failed
    """
    db = DB_Actions()
    if key is None:
        # get key from db. If there is a key, the login is valid
        result = db._get_key(user, server)
        return result
    else:
        result = db._email_login(user, server, key)
        if result == EMAIL_CONST.IMAP_CONN_FAIL:
            return EMAIL_CONST.IMAP_CONN_FAIL
        # add key.
        db._add_email_server(user, server, key)
        return EMAIL_CONST.IMAP_CONN_SUCCESS


def _email_save_key(user, server, key=None):
    """
    Save email key.
    """
    db = DB_Actions()
    result = db._email_login(user, server, key)
    if result == EMAIL_CONST.IMAP_CONN_FAIL:
        return EMAIL_CONST.IMAP_CONN_FAIL
    db._add_email_server(user, server, key)
    return EMAIL_CONST.IMAP_CONN_SUCCESS


def _email_move_to_gmail(user, server):
    """Not implemented"""
    pass


def _email_move_to_database(user, server):
    """
    Move emails from mail server to the database.
    """
    db = DB_Actions()
    user_key = db._get_key(user, server)
    if user_key == EMAIL_CONST.IMAP_CONN_FAIL:
        return EMAIL_CONST.IMAP_CONN_FAIL

    gather = Gather(user, server, user_key)
    status = gather.gather()

    if status == EMAIL_CONST.IMAP_CONN_FAIL:
        print("STATUS: failed to check IMAP to move to db")
        return EMAIL_CONST.IMAP_CONN_FAIL
    elif status == EMAIL_CONST.NO_EMAILS:
        print("STATUS: no emails to move to db")
        return EMAIL_CONST.NO_EMAILS

    emails = gather.get_emails()
    db._add_emails(user, emails)

    return EMAIL_CONST.IMAP_CONN_SUCCESS


def _email_get_by_eid(user, email_id):
    """
    Retrieve one email for the history detail view.
    """
    db = DB_Actions()
    row = db._gather_email(user, email_id)
    if not row:
        return None

    (id_, sender_json, category, data_json, collected_date, delete_date) = row

    # sender_json and data_json may be dict or JSON string
    if isinstance(sender_json, str):
        try:
            sender_json = json.loads(sender_json)
        except Exception:
            sender_json = {}

    if isinstance(data_json, str):
        try:
            data_json = json.loads(data_json)
        except Exception:
            data_json = {}

    return {
        "id": id_,
        "sender": sender_json,
        "category": category,
        "data": data_json,
        "collected_date": _to_iso(collected_date),
        "delete_date": _to_iso(delete_date),
    }


def _email_get_by_page(user, page, cat, per_page=50):
    """
    Returns a list of email dicts for a given user, ordered newest → oldest.
    Flask JSON cannot serialize datetime, so we convert them to strings.
    """
    offset = (page - 1) * per_page
    db = DB_Actions()

    if not cat:
        rows = db._gather_email_by_page(uid=user, limit=per_page, offset=offset)
    else:
        rows = db._gather_data_by_category(
            user_id=user, category=cat, limit=per_page, offset=offset
        )

    emails = []
    for r in rows:
        # r layout:
        # 0: id
        # 1: sender_add (jsonb)
        # 2: category
        # 3: data (jsonb)
        # 4: collected_date
        # 5: delete_date
        sender_val = r[1]
        data_val = r[3]

        if isinstance(sender_val, str):
            try:
                sender_val = json.loads(sender_val)
            except Exception:
                sender_val = {}

        if isinstance(data_val, str):
            try:
                data_val = json.loads(data_val)
            except Exception:
                data_val = {}

        email = {
            "id": r[0],
            "sender": sender_val,
            "category": r[2],
            "subject": data_val.get("subject", ""),
            "preview": data_val.get("preview", ""),
            "collected_date": _to_iso(r[4]),
            "delete_date": _to_iso(r[5]),
        }
        emails.append(email)

    return emails


def _email_get_dashboard(user, per_category=3):
    """
    Returns category sections for the dashboard page:
    the newest few emails per category.
    """
    db = DB_Actions()

    # retrieve categories (JSON stored in user_data.priv_cats)
    raw_cats = db._gather_categories((user, ""))

    if isinstance(raw_cats, str):
        try:
            categories = json.loads(raw_cats)
        except Exception:
            categories = []
    else:
        categories = raw_cats or []

    sections = []

    for cat in categories:
        if not isinstance(cat, dict):
            continue

        name = cat.get("name")
        if not name:
            continue

        display_name = cat.get("display_name", name)
        color = cat.get("color") or "#4a90e2"

        rows = db._gather_data_by_category(
            user_id=user, category=name, limit=per_category, offset=0
        )

        emails = []
        for r in rows:
            sender_json = r[1]
            data_json = r[3]

            if isinstance(sender_json, str):
                try:
                    sender_json = json.loads(sender_json)
                except Exception:
                    sender_json = {}

            if isinstance(data_json, str):
                try:
                    data_json = json.loads(data_json)
                except Exception:
                    data_json = {}

            emails.append({
                "id": r[0],
                "sender_name": sender_json.get("sender_name", ""),
                "sender_addr": sender_json.get("sender_addr", ""),
                "subject": data_json.get("subject", "No subject"),
                "preview": data_json.get("preview", ""),
                "collected_date": _to_iso(r[4]),
                "delete_date": _to_iso(r[5]),
            })

        if emails:
            sections.append({
                "category": name,
                "display_name": display_name,
                "color": color,
                "emails": emails,
            })

    return sections
