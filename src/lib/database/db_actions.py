import json
from datetime import datetime as dt
from datetime import timezone as tz

from src.lib import EMAIL_CONST, DB_CONST
from src.lib.database.db_conn import DB_Connection

class DB_Actions:
    conn = DB_Connection()

# login 
    def _check_pass(self, user_id, password):
        '''
        Check if user is in the database. return missing account, success, or incorrect account info
        '''
        query = 'SELECT user_pass FROM public.user_data WHERE user_id = %s'
        check = self.conn._get(query=query, args=(user_id,))
        print(check)

        if check is None:
            return EMAIL_CONST.MISSING_ACCOUNT
        elif check == password:
            return EMAIL_CONST.LOGIN_SUCCESS
        else:
            return EMAIL_CONST.INCORRECT_ACCOUNT_INFO
        
    def _add_new_user(self, user_id, password):
        '''
        add a new credential to the db
        '''
        query = '''INSERT INTO public.user_data (user_id, user_pass, priv_cats)
        VALUES (%s, %s, %s)''' # TODO: hashing?
        return self.conn._set(query, (user_id, password, "{}",))
    
# get
    def _gather_data_by_user(self, user_id):
        '''
        This functions uses SQL to gather all emails by user_id.
        Ensure in previous function that user_id == login id
        '''
        query = 'SELECT * FROM public.email_data WHERE user_id = %s'
        data = self.conn._get(query, (user_id,))

        return [list(t) for t in data]

    def _gather_data_by_sender(self, user_id, sender_id):
        '''
        This functions uses SQL to gather all emails by sender.
        Ensure in previous function that user_id == login id
        '''
        query = 'SELECT * FROM public.email_data WHERE user_id = %s AND sender_id = %s'
        data = self.conn._get(query, (user_id, sender_id,))

        return [list(t) for t in data]

    def _gather_data_by_category(self, category):
        '''
        This functions uses SQL to gather all emails by category.
        Ensure in previous function that user_id == login id for private categories
        '''
        query = 'SELECT * FROM public.email_data WHERE category = %s'
        data = self.conn._get(query, (category,))

        return [list(t) for t in data]
    
    def _gather_categories(self, credentials):
        '''
        get categories
        
        :param credentials: tuple of username and password
        '''
        query = '''SELECT priv_cats FROM public.user_data
        WHERE user_id = %s AND user_pass = %s''' # TODO: hashing?
        data = self.conn._get(query, credentials)
        if not data:
            return []
        try:
            print("DEBUG: ")
            print(data[0][0])
            categories = json.loads(data[0][0])
        except json.JSONDecodeError:
            print("ERROR: failed to parse categories JSON: " + data)
            categories = None
        return categories
    
    def _gather_user_key(self, credentials) -> str:

        query = '''SELECT user_key FROM public.user_data
        WHERE user_id = %s AND user_pass = %s''' # TODO: hashing?
        data = self.conn._get(query, credentials)
        return data[0][0]
    
    def _gather_email(self, uid, eid):
        '''
        get an email based on the email id. user id must match
        
        :param uid: user id, the email
        :param eid: email id
        '''
        query = '''SELECT id, sender_add, category, data, collected_date, delete_date
        FROM public.email_data
        WHERE user_id = %s AND id = %s
        LIMIT 1;'''
        row = self.conn._get(query, (uid, eid,))

        # If nothing found, return None
        if not row or not row[0]:
            return None
        return row[0]
    
    def _gather_email_by_page(self, uid, limit, offset):
        '''
        Docstring for _gather_email_by_page
        
        :param uid: username
        :param limit: how many emails to return
        :param offset: where to start from
        '''
        query = '''SELECT id, sender_add, category, data, collected_date, delete_date FROM email_data
        WHERE user_id = %s
        ORDER BY collected_date DESC
        LIMIT %s OFFSET %s'''
        rows = self.conn._get(query, (uid, limit, offset,))
        return rows


# set
    def _add_email_data(self, data):
        '''
        The param data should ideally be a single tuple or 1D array
        '''
        # Maybe format into tuple before
        query = '''INSERT INTO public.email_data (user_id, sender_add, category, data, delete_date) 
        VALUES (%s, %s::jsonb, %s, %s::jsonb, %s)'''
        result = self.conn._set(query=query, args=data)
        
        if result == DB_CONST.DB_ERROR:
            print('Unable to write data')

    def _add_categories(self, credentials, cats):
        '''
        get categories
        
        :param credentials: tuple of username, password
        '''
        query = '''INSERT INTO public.user_data (user_id, user_pass, priv_cats)
        VALUES (%s, %s, %s)
        ON CONFLICT (user_id) DO UPDATE SET priv_cats = EXCLUDED.priv_cats''' # TODO: hashing?
        data = self.conn._set(query, credentials + (cats,)) # TODO: alex, can you check this logic?
        return data
    
    def _add_email_key(self, credentials, key):
        '''
        saves or updates the user key to their email
        
        :param credentials: tuple of username, password
        '''
        query = '''INSERT INTO public.user_data (user_id, user_pass, user_key)
        VALUES (%s, %s, %s)
        ON CONFLICT (user_id) DO UPDATE SET user_key = EXCLUDED.user_key'''
        data = self.conn._set(query, credentials + (key,)) # TODO: alex, can you check this logic?
        return data

#actions
    def _delete_old_emails(self):
        now = dt.now(tz.utc)
        query = 'DELETE FROM public.email_data WHERE delete_date < %s'
        result = self.conn._set(query, (now,))

        now.astimezone()
        print(f'All emails past {now.strftime('%m/%d/%Y')} have been deleted.')

        if result == DB_CONST.DB_ERROR:
            print('Email delete error')
