# Matt 4:4
# this will be experimental where the user can login into inbox insight. i moved the imap login things to email/email_actions.py -tolu
from src.lib.database.db_actions import DB_Actions
from src.lib import DB_CONST, EMAIL_CONST

def _user_create_account(user, password):
    'checks if account exist. stores if new'
    db = DB_Actions()
    exist = db._get_pass(user_id=user, password=password)
    if exist != EMAIL_CONST.LOGIN_SUCCESS: # does not exist
        print("STATUS: creating a new user")
        db._add_new_user(user_id=user, password=password)
    

def _user_login(user, password):
    '''
    checks if valid account for user and password. returns if exist, does not exist, or incorrect info
    '''
    db = DB_Actions()
    check = db._get_pass(user)
    print(check)

    if check is None:
        return EMAIL_CONST.MISSING_ACCOUNT
    elif check == password:
        return EMAIL_CONST.LOGIN_SUCCESS
    else:
        return EMAIL_CONST.INCORRECT_ACCOUNT_INFO
                                       