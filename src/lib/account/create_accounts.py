# Matt 4:4
from src.lib.database.db_actions import DB_Actions
from src.lib.email_scraper.email_scraper import Gather
from src.lib import DB_CONST, EMAIL_CONST

def _create_account(user, password, server):
    'checks if account exist. stores if new'
    db = DB_Actions()
    exist = db._check_pass(user_id=user, password=password)
    if exist != EMAIL_CONST.LOGIN_SUCCESS: # does not exist
        db._add_new_user(user_id=user, password=password)
    

def _login(user, password, server):
    '''
    Checks basic connection.
        Returns: 
        - 0: Success 
        - 3: IMAP server connection failed
    '''
    user_connection_check = Gather(user, password, server)

    try:
        user_connection_check._connect()
        # Disconnects for security
        user_connection_check._disconnect()
    except:
        return EMAIL_CONST.IMAP_CONN_FAIL
    
    return EMAIL_CONST.LOGIN_SUCCESS