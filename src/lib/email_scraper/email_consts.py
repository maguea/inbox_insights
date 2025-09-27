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