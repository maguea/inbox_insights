# Matt 4:4

from dotenv import set_key, load_dotenv
from pathlib import Path
from lib.email_scraper.email_scraper import Gather
from lib.email_scraper.email_consts import EMAIL_CONST
import os

def _create_account(user, password, server):
    'Creates and stores account info into dotenv file'
    env_file_path = Path('.env')
    set_key(dotenv_path=env_file_path, key_to_set='CLIENT_USER', value_to_set='some_value')
    set_key(dotenv_path=env_file_path, key_to_set='CLIENT_PASS', value_to_set='new_secret')
    set_key(dotenv_path=env_file_path, key_to_set='CLIENT_SERVER', value_to_set='example.imap.com')

def _login(user, password):
    '''
    Checks basic connection.
        Returns: 
        - 0: Success 
        - 1: Incorrect Password or Email 
        - 2: Account not set up/not saved 
        - 3: IMAP server connection failed
    '''
    load_dotenv()

    try:
        check_user = os.getenv('CLIENT_USER')
    except:
        return EMAIL_CONST.MISSING_ACCOUNT
    
    check_pass = os.getenv('CLIENT_PASS')
    check_server = os.getenv('CLIENT_SERVER')

    if check_pass != password or check_user != user:
        return EMAIL_CONST.INCORRECT_ACCOUNT_INFO
    
    user_connection_check = Gather(check_user, check_pass, check_server)

    try:
        user_connection_check._connect()
        # Disconnects for security
        user_connection_check._disconnect()
    except:
        return EMAIL_CONST.IMAP_CONN_FAIL
    
    return EMAIL_CONST.LOGIN_SUCCESS

def _check_env():
    '''
    Checks basic connection.
        Returns: 
        - 0: Success 
        - 1: Incorrect Password or Email 
        - 2: Account not set up/not saved 
        - 3: IMAP server connection failed
    '''
    load_dotenv()

    try:
        os.getenv('CLIENT_USER')
    except:
        return False
    return True