import json

from src.lib import EMAIL_CONST
from src.lib.database.db_actions import DB_Actions
from src.lib.email.email_scraper import Gather


def _email_login(user, server, key=None):
    '''
    Checks basic connection.
        Returns: 
        - 0: Success 
        - 3: IMAP server connection failed
    '''
    db = DB_Actions()
    if key is None:
        key = db._gather_user_key((user, "",))  # TODO: update logic for additional emails
        print("STATUS: getting key from db..." + key)
    user_connection_check = Gather(user, key, server)

    try:
        user_connection_check._connect()
        # Disconnects for security
        user_connection_check._disconnect()
    except Exception:
        print("ERROR: couldnt connect to imap..")
        return EMAIL_CONST.IMAP_CONN_FAIL

    return EMAIL_CONST.LOGIN_SUCCESS


def _email_save_key(user, key):
    '''
    saves or updates the key for the user
    
    :param key: key to be saved
    '''
    db = DB_Actions()
    return db._add_email_key((user, ""), key)  # TODO: update logic for additional emails


def _email_get_by_eid(user, email_id):
    db = DB_Actions()
    row = db._gather_email(user, email_id)
    (id_, sender_json, category, data_json, collected_date, delete_date) = row

    # psycopg2 may already give dicts for jsonb;
    # but if your wrapper gives strings, parse them:
    if isinstance(sender_json, str):
        sender_json = json.loads(sender_json)

    if isinstance(data_json, str):
        data_json = json.loads(data_json)

    return {
        "id": id_,
        "sender": sender_json,        # dict
        "category": category,         # string or None
        "data": data_json,            # dict: {subject, preview, data}
        "collected_date": collected_date,
        "delete_date": delete_date
    }


def _email_get_by_page(user, page, cat, per_page=50):
    """
    Returns a list of email dicts for a given user, ordered from newest to oldest,
    using LIMIT/OFFSET.
    """
    offset = (page - 1) * per_page
    db = DB_Actions()

    if not cat:
        rows = db._gather_email_by_page(uid=user, limit=per_page, offset=offset)
    else:
        rows = db._gather_data_by_category(user_id=user, category=cat, limit=per_page, offset=offset)

    emails = []
    for r in rows:
        # r layout (from db_actions):
        # 0: id
        # 1: sender_add  (jsonb)
        # 2: category
        # 3: data        (jsonb: subject/preview/body)
        # 4: collected_date
        # 5: delete_date
        sender_val = r[1]
        data_val = r[3]

        if isinstance(sender_val, str):
            try:
                sender_val = json.loads(sender_val)
            except json.JSONDecodeError:
                sender_val = {}

        if isinstance(data_val, str):
            try:
                data_val = json.loads(data_val)
            except json.JSONDecodeError:
                data_val = {}

        email = {
            "id": r[0],
            "sender": sender_val,                         # dict with sender_name/sender_addr
            "category": r[2],
            "subject": data_val.get("subject", ""),
            "preview": data_val.get("preview", ""),
        }
        emails.append(email)

    return emails
