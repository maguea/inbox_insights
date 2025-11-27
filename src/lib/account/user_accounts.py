# Matt 4:4
# this will be experimental where the user can login into inbox insight. i moved the imap login things to email/email_actions.py -tolu
from src.lib.database.db_actions import DB_Actions
from src.lib import DB_CONST, EMAIL_CONST

def _user_create_account(user, password):
    'checks if account exist. stores if new'
    db = DB_Actions()
    exist = db._check_pass(user_id=user, password=password)
    if exist != EMAIL_CONST.LOGIN_SUCCESS: # does not exist
        print("STATUS: creating a new user")
        db._add_new_user(user_id=user, password=password)
    

def _login(user, password):
    '''
    Checks basic connection.
        Returns: 
        - 0: Success 
        - 3: IMAP server connection failed
    '''
    db = DB_Actions()
    return db._check_pass((user, password))