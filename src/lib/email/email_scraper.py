# Matt 4:4 - Modified to return formatted email list

import imaplib, email, json
from email.header import decode_header
from email.utils import parseaddr, parsedate_to_datetime
from datetime import datetime

from src.lib import EMAIL_CONST
from src.lib.database.db_actions import DB_Actions

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
        '''
        Gets sender (alias connected to email)
        '''
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
        '''
        Returns sender info as a dict:
        {
            "name": "John Doe",
            "address": "john@acme.com"
        }
        If parsing fails, fields may be empty strings.
        '''
        from_header = msg.get('From', '') or ''
        name, addr = parseaddr(from_header)

        name = self._decode_header_value(name) if name else ''
        addr = addr or ''

        return {
            "name": name,
            "address": addr
        }

    def _get_subject(self, msg):
        '''
        Returns decoded subject line
        '''
        subject = msg.get('Subject', 'No Subject')
        return self._decode_header_value(subject)
    
    def _get_category(self, sender):
        category = DB_Actions._get_cat_by_sender(sender)
        return category

    def _get_date_info(self, msg):
        '''
        Returns formatted date and timestamp
        Returns: (timestamp_str, date_str)
        Example: ("2:30 PM", "Oct 1, 2025")
        '''
        date_header = msg.get('Date')
        if not date_header:
            return "Unknown", "Unknown"
        
        try:
            dt = parsedate_to_datetime(date_header)
            # Use cross-platform formatting
            hour = dt.strftime("%I").lstrip("0")  # Remove leading zero manually
            timestamp = f"{hour}:{dt.strftime('%M %p')}"  # "2:30 PM"
        
            day = str(dt.day)  # No leading zero
            date_str = f"{dt.strftime('%b')} {day}, {dt.strftime('%Y')}"  # "Oct 1, 2025"
            return timestamp, date_str
        except Exception as e:
            print(f"Date parsing error: {e}")  # Debug
            return "Unknown", "Unknown"

    def _get_plain_text(self, msg):
        '''
        Returns plain text content
        '''
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                disp = str(part.get('Content-Disposition') or '').lower()
                if ctype == 'text/plain' and 'attachment' not in disp:
                    payload = part.get_payload(decode=True)
                    if payload:
                        return payload.decode(part.get_content_charset() or 'utf-8', errors='ignore').strip()
            # Fallback to HTML if no plain text
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

    def _get_html_body(self, msg):
        '''
        Returns HTML content, or wraps plain text in <p> tags
        '''
        if msg.is_multipart():
            # Try to get HTML part first
            for part in msg.walk():
                ctype = part.get_content_type()
                disp = str(part.get('Content-Disposition') or '').lower()
                if ctype == 'text/html' and 'attachment' not in disp:
                    payload = part.get_payload(decode=True)
                    if payload:
                        return payload.decode(part.get_content_charset() or 'utf-8', errors='ignore').strip()
            
            # Fallback to plain text wrapped in <p>
            plain = self._get_plain_text(msg)
            if plain:
                # Simple conversion: wrap paragraphs in <p> tags
                paragraphs = plain.split('\n\n')
                return ''.join(f'<p>{p.strip()}</p>' for p in paragraphs if p.strip())
            return ''
        else:
            ctype = msg.get_content_type()
            if ctype == 'text/html':
                payload = msg.get_payload(decode=True)
                if payload:
                    return payload.decode(msg.get_content_charset() or 'utf-8', errors='ignore').strip()
            else:
                # Plain text - wrap in <p>
                plain = self._get_plain_text(msg)
                if plain:
                    paragraphs = plain.split('\n\n')
                    return ''.join(f'<p>{p.strip()}</p>' for p in paragraphs if p.strip())
                return ''

    def _get_attachments(self, msg):
        '''
        Returns list of attachment filenames
        '''
        attachments = []
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                disp = str(part.get('Content-Disposition') or '')
                if 'attachment' in disp.lower():
                    filename = part.get_filename()
                    if filename:
                        # Decode filename if needed
                        filename = self._decode_header_value(filename)
                        attachments.append(filename)
        return attachments

    def _create_preview(self, text, length=60):
        '''
        Create a preview from text content
        '''
        if not text:
            return "No content"
        
        # Remove HTML tags if present
        import re
        clean = re.sub(r'<[^>]+>', '', text)
        clean = clean.strip()
        
        if len(clean) <= length:
            return clean
        return clean[:length] + "..."

    def _fetch_unread_and_mark_seen(self):
        '''
        Fetch unread emails and return as a list in the format:
        [
            {
                "sender": {
                    "name": "John Doe",
                    "address": "john@acme.com"
                },
                "subject": "Q4 Launch Plan",
                "preview": "Here's the quick summary...",
                "timestamp": "2:30 PM",
                "date": "Oct 1, 2025",
                "body": "<p><b>Hi team,</b></p>...",
            }
        ]
        '''
        print("Starting fetch...")
        self._connect()
        try:
            print("Searching for unread emails...")
            status, data = self.conn.search(None, 'UNSEEN')
            print(f"Search status: {status}, found: {data}")
            if status != 'OK':
                return []
    
            ids = data[0].split()
            print(f"Found {len(ids)} unread email IDs")
            if not ids:
                return []
    
            result = []
            
            for eid in ids:
                print(f"Fetching email {eid}...")
                status, msg_data = self.conn.fetch(eid, '(RFC822)')
                print(f"Fetch status: {status}")
                if status != 'OK' or not msg_data or not isinstance(msg_data[0], tuple):
                    print(f"Skipping email {eid}")
                    continue
                
                raw_msg = msg_data[0][1]
                msg = email.message_from_bytes(raw_msg)
                print(f"Parsing email from: {msg.get('From', 'unknown')}")
    
                # Extract all fields
                sender = self._get_sender(msg)  # now a dict
                subject = self._get_subject(msg)
                print(f"  Subject: {subject}")
                timestamp, date_str = self._get_date_info(msg)
                body = self._get_html_body(msg)
                print(f"  Body length: {len(body)}")
                preview = self._create_preview(body)
                category = self._get_category(sender)
    
                # Build email object (with structured sender)
                email_obj = {
                    "sender": sender,
                    "subject": subject,
                    "preview": preview,
                    "timestamp": timestamp,
                    "date": date_str,
                    "body": body,
                    "category" : category,
                }
                
                result.append(email_obj)
                print(f"  ✅ Email from {sender.get('address') or sender.get('name') or 'unknown'} processed")
    
                # Mark as read (uncomment to enable)
                # self.conn.store(eid, '+FLAGS', r'(\Seen)')
    
            print(f"Total emails fetched: {len(result)}")
            return result
    
        finally:
            print("Disconnecting...")
            self._disconnect()
            print("Disconnected")




# Example usage
if __name__ == '__main__':
    USER = EMAIL_CONST.GMAIL['user']
    PASS = EMAIL_CONST.GMAIL['pass']
    SERVER = EMAIL_CONST.GMAIL['server']
    
    test = Gather(USER, PASS, SERVER)
    test_emails = test._fetch_unread_and_mark_seen()
    
    print(json.dumps(test_emails, indent=2))