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

class DB_CONST:
    PG_DB = os.getenv('PG_DB')
    PG_USER = os.getenv('PG_USER')
    PG_PASS = os.getenv('PG_PASS')
    PG_HOST = os.getenv('PG_HOST')
    PG_PORT = os.getenv('PG_PORT')

    DB_ERROR = 5


def get_error_message(result_code):
    error_messages = {
        0: 'Success',
        1: "Incorrect email or password",
        2: "Account not set up properly",
        3: "Cannot connect to IMAP server",
        4: "Read Fail", # TODO: add meaningful message
        5: "Database error" # TODO: add meaningful message
    }
    return error_messages.get(result_code, "Unknown error occurred")