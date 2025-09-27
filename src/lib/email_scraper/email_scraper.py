# Matt 4:4

import imaplib, email
from email.header import decode_header
from email.utils import parseaddr
from email_consts import EMAIL_CONST


class Gather:
    def __init__(self, username, password, imap_server, mailbox='INBOX'):
        self.username = username
        self.password = password
        self.imap_server = imap_server
        self.mailbox = mailbox
        self.conn = None

    def _connect(self):
        '''Connect and log in to the IMAP server.'''
        self.conn = imaplib.IMAP4_SSL(self.imap_server)
        self.conn.login(self.username, self.password)
        self.conn.select(self.mailbox)

    def _disconnect(self):
        '''Close and log out safely.'''
        if self.conn:
            try:
                self.conn.close()
            except Exception:
                pass
            self.conn.logout()
            self.conn = None

    def _decode_header_value(self, value):
        if not value:
            return ''
        parts = decode_header(value)
        decoded = []
        for text, enc in parts:
            if isinstance(text, bytes):
                decoded.append(text.decode(enc or 'utf-8', errors='ignore'))
            else:
                decoded.append(text)
        return ''.join(decoded)

    def _get_sender(self, msg):
        name, addr = parseaddr(msg.get('From', ''))
        name = self._decode_header_value(name)
        return addr or name or 'unknown'

    def _get_plain_text(self, msg):
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                disp = str(part.get('Content-Disposition') or '').lower()
                if ctype == 'text/plain' and 'attachment' not in disp:
                    payload = part.get_payload(decode=True)
                    if payload:
                        return payload.decode(part.get_content_charset() or 'utf-8', errors='ignore').strip()
            for part in msg.walk():
                if part.get_content_type() == 'text/html':
                    payload = part.get_payload(decode=True)
                    if payload:
                        return payload.decode(part.get_content_charset() or 'utf-8', errors='ignore').strip()
            return ''
        else:
            payload = msg.get_payload(decode=True)
            if payload is None:
                return ''
            return payload.decode(msg.get_content_charset() or 'utf-8', errors='ignore').strip()

    def fetch_unread_and_mark_seen(self, limit=None):
        '''
        Fetch unread emails, mark them as read, and return a dict:
            {'sender@example.com': {'content': 'message'}}
        '''
        self._connect()
        try:
            status, data = self.conn.search(None, 'UNSEEN')
            if status != 'OK':
                return {}

            ids = data[0].split()
            if not ids:
                return {}

            if limit is not None:
                ids = ids[:limit]

            result = {}
            for eid in ids:
                status, msg_data = self.conn.fetch(eid, '(RFC822)')
                if status != 'OK' or not msg_data or not isinstance(msg_data[0], tuple):
                    continue

                raw_msg = msg_data[0][1]
                msg = email.message_from_bytes(raw_msg)

                sender = self._get_sender(msg)
                content = self._get_plain_text(msg)

                result[sender] = {'content': content}

                # Mark as read
                self.conn.store(eid, '+FLAGS', r'(\Seen)')

            return result

        finally:
            self._disconnect()


# Example usage
if __name__ == '__main__':
    USER = EMAIL_CONST.GMAIL['user']
    PASS = EMAIL_CONST.GMAIL['pass']
    SERVER = EMAIL_CONST.GMAIL['server']
    g = Gather(USER, PASS, SERVER)
    unread = g.fetch_unread_and_mark_seen(limit=5)
    print(unread)
