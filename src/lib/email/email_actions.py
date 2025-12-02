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
    if key == None:
        key = db._gather_user_key((user, "",)) #TODO: update logic for additional emails
        print("STATUS: getting key from db..." + key)
    user_connection_check = Gather(user, key, server)

    try:
        user_connection_check._connect()
        # Disconnects for security
        user_connection_check._disconnect()
    except:
        print("ERROR: couldnt connect to imap..")
        return EMAIL_CONST.IMAP_CONN_FAIL
    
    return EMAIL_CONST.LOGIN_SUCCESS

def _email_save_key(user, key):
    '''
    saves or updates the key for the user
    
    :param key: key to be saved
    '''
    db = DB_Actions()
    return db._add_email_key((user, ""), key) #TODO: update logic for additional emails

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
        "sender": sender_json,       # dict
        "category": category,        # string or None
        "data": data_json,           # dict: {subject, preview, data}
        "collected_date": collected_date,
        "delete_date": delete_date
    }

def _email_get_by_page(user, page, per_page=50):
    """
    Returns a list of email dicts for a given user, ordered from newest to oldest,
    using LIMIT/OFFSET.
    """
    offset = (page - 1) * per_page
    db = DB_Actions()
    rows = db._gather_email_by_page(uid=user, limit=per_page, offset=offset)

    # Turn rows into simple dicts if `rows` are tuples/records
    emails = []
    for r in rows:
        email = {
            "id": r[0],
            "sender": r[1], # has sender_addr and sender_name
            "subject": r[3]["subject"],
            "preview": r[3]["preview"]
        }
        print(email)
        emails.append(email)
    return emails

    