from datetime import datetime as dt
from datetime import timezone as tz

from src.lib import EMAIL_CONST, DB_CONST
from src.lib.database.db_conn import DB_Connection

class DB_Actions:
    conn = DB_Connection()

# login 
    def _get_pass(self, user_id):
        '''
        gets password for user
        '''
        query = 'SELECT user_pass FROM public.user_data WHERE user_id = %s'
        password = self.conn._get(query=query, args=(user_id,))
        # print(password)
        try:
            return password[0][0]
        except:
            return None
        
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

    def _gather_data_by_category(self, category, limit, offset):
        '''
        This functions uses SQL to gather all emails by category.
        Ensure in previous function that user_id == login id for private categories
        '''
        query = 'SELECT * FROM public.email_data WHERE category = %s ORDER BY collected_date DESC LIMIT %s OFFSET %s'
        data = self.conn._get(query, (category, limit, offset,))

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
            print("STATUS: empty category")
            print(data)
            return []
        try:
            categories = data[0][0]
        except:
            print("ERROR: category failed to be retrieved")
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
    
    def _gather_email_by_page(self, uid, category, limit, offset):
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
    
    def _get_cat_by_sender(self, sender):
        query = '''SELECT category FROM public.email_data WHERE sender_id = %s LIMIT 1;'''
        rows = self.conn._get(query, (sender,))
        return rows[0][0]


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
        VALUES (%s, %s, %s::jsonb)
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
    def _delete_email(self, user_id, email_id):
        '''
        Delete a single email by email_id and user_id.
        Ensures user owns the email before deletion.
        
        :param user_id: the user id
        :param email_id: the email id to delete
        :return: True if successful, False if error or email not found
        '''
        query = 'DELETE FROM public.email_data WHERE user_id = %s AND id = %s'
        result = self.conn._set(query, (user_id, email_id,))

        if result == DB_CONST.DB_ERROR:
            print(f'Error deleting email {email_id} for user {user_id}')
            return False
        
        print(f'Email {email_id} deleted for user {user_id}')
        return True

    def _delete_old_emails(self):
        now = dt.now(tz.utc)
        query = 'DELETE FROM public.email_data WHERE delete_date < %s'
        result = self.conn._set(query, (now,))

        now.astimezone()
        print(f'All emails past {now.strftime('%m/%d/%Y')} have been deleted.')

        if result == DB_CONST.DB_ERROR:
            print('Email delete error')

    def _categorize(self, user, sender, category):
        query = '''UPDATE public.email_data SET category = %s WHERE user_id = %s AND sender_id = %s;'''
        check = self.conn._set(query, (category, user, sender,))
        print(check)
