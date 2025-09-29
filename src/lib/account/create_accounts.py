# Matt 4:4

from dotenv import set_key, load_dotenv
from pathlib import Path
from lib.email_scraper.email_scraper import Gather
import os

def _create_account(user, password, server):
    env_file_path = Path('.env')
    set_key(dotenv_path=env_file_path, key_to_set='CLIENT_USER', value_to_set='some_value')
    set_key(dotenv_path=env_file_path, key_to_set='CLIENT_PASS', value_to_set='new_secret')
    set_key(dotenv_path=env_file_path, key_to_set='CLIENT_SERVER', value_to_set='example.imap.com')

def _login(user, password):
    load_dotenv()
    check_user = os.getenv('CLIENT_USER')
    check_pass = os.getenv('CLIENT_PASS')
    check_server = os.getenv('CLIENT_SERVER')

    if check_pass != password:
        return 'LOGIN ERROR: Incorrect Password'
    
    user_connection_check = Gather(check_user, check_pass, check_server)

    try:
        user_connection_check._connect()
    except Exception as e:
        return f'CONNECTION ERROR: {e}'
    
    return 'SUCCESS'
