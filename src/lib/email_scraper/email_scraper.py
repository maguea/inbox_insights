# Matt 4:4

import imaplib
from dotenv import load_dotenv
import os

load_dotenv()

gmail = {
    "user" : os.getenv("GMAIL_USER"),
    "pass" : os.getenv("GMAIL_PASS")
}

outlook = {
    "user" : os.getenv("OUTLOOK_USER"),
    "pass" : os.getenv("OUTLOOK_PASS")
}

print(f"gmail info: {gmail}")
print(f"outlook info: {outlook}")