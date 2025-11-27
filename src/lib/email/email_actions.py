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