# Matt 4:4

from dotenv import load_dotenv
import os

class EMAIL_CONST:

    load_dotenv()

    GMAIL = {
        'user' : os.getenv('GMAIL_USER'),
        'pass' : os.getenv('GMAIL_APP_KEY'),
        'server' : 'imap.gmail.com'
    }

    OUTLOOK = {
        'user' : os.getenv('OUTLOOK_USER'),
        'pass' : os.getenv('OUTLOOK_PASS'),
        'server' :  'imap-mail.outlook.com'
    }

    LOGIN_SUCCESS = 0
    INCORRECT_ACCOUNT_INFO = 1
    MISSING_ACCOUNT = 2
    IMAP_CONN_FAIL = 3
    READ_FAIL = 4

class DB_Const:
    PG_DB = os.getenv('PG_DB')
    PG_USER = os.getenv('PG_USER')
    PG_PASS = os.getenv('PG_PASS')
    PG_HOST = os.getenv('PG_HOST')
    PG_PORT = os.getenv('PG_PORT')

    DB_ERROR = 5
