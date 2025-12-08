from datetime import datetime as dt
from datetime import timezone as tz
from datetime import timedelta
import json

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
        VALUES (%s, %s, %s)'''  # TODO: hashing?
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

    def _gather_data_by_category(self, user_id, category, limit, offset):
        '''
        This functions uses SQL to gather all emails by category.
        Ensure in previous function that user_id == login id for private categories
        '''
        query = '''SELECT id, sender_add, category, data, collected_date, delete_date 
        FROM public.email_data 
        WHERE user_id = %s AND category = %s 
        ORDER BY collected_date DESC LIMIT %s OFFSET %s'''
        data = self.conn._get(query, (user_id, category, limit, offset,))

        return [list(t) for t in data]
    
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
    
    def _gather_categories(self, credentials):
        '''
        get categories
        
        :param credentials: tuple of username and password
        '''
        query = '''SELECT priv_cats FROM public.user_data
        WHERE user_id = %s AND user_pass = %s'''  # TODO: hashing?
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
        WHERE user_id = %s AND user_pass = %s'''  # TODO: hashing?
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
        
    def _get_cat_by_sender(self, uid, sender):
        query = '''SELECT cat->>'name'
        FROM public.user_data
        CROSS JOIN LATERAL jsonb_array_elements(priv_cats) AS cat
        CROSS JOIN LATERAL jsonb_array_elements_text(cat->'emails') AS email(pattern)
        WHERE user_id = %s
        AND %s LIKE REPLACE(pattern, '*', '%%')
        LIMIT 1;'''
        rows = self.conn._get(query, (uid, sender))
        try:
            print(rows)
            return rows[0][0]
        except Exception as exc:
            print(exc)
            return 'misc'

# set
    def _delete_email(self, user, eid):
        query = """ DELETE FROM public.email_data
        WHERE user_id = %s AND id = %s
        """
        result = self.conn._set(query=query, args=(user, eid))
        
        if result == DB_CONST.DB_ERROR:
            print('Unable to write data')


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
        Save categories and then recalculate delete_date for this user's emails.
        
        :param credentials: tuple of username, password
        '''
        query = '''INSERT INTO public.user_data (user_id, user_pass, priv_cats)
        VALUES (%s, %s, %s::jsonb)
        ON CONFLICT (user_id) DO UPDATE SET priv_cats = EXCLUDED.priv_cats'''  # TODO: hashing?
        data = self.conn._set(query, credentials + (cats,))  # TODO: alex, can you check this logic?

        # After saving categories, update delete_date for all this user's emails
        user_id = credentials[0]
        try:
            self._recalculate_delete_dates_for_user(user_id)
        except Exception as e:
            # Don't crash the request if this fails; just log it.
            print("WARNING: failed to recalculate delete dates:", repr(e))

        return data
    
    def _add_email_key(self, credentials, key):
        '''
        saves or updates the user key to their email
        
        :param credentials: tuple of username, password
        '''
        query = '''INSERT INTO public.user_data (user_id, user_pass, user_key)
        VALUES (%s, %s, %s)
        ON CONFLICT (user_id) DO UPDATE SET user_key = EXCLUDED.user_key'''
        data = self.conn._set(query, credentials + (key,))  # TODO: alex, can you check this logic?
        return data

#actions
    def _delete_old_emails(self):
        now = dt.now(tz.utc)
        query = 'DELETE FROM public.email_data WHERE delete_date < %s'
        result = self.conn._set(query, (now,))

        now.astimezone()
        # fixed quoting in f-string
        print(f"All emails past {now.strftime('%m/%d/%Y')} have been deleted.")

        if result == DB_CONST.DB_ERROR:
            print('Email delete error')

    def _categorize(self, user, sender, category):
        query = '''UPDATE public.email_data SET category = %s WHERE user_id = %s AND sender_id = %s;'''
        check = self.conn._set(query, (category, user, sender,))
        print(check)

    # ------ new helper: recalc delete_date after category changes ------
    def _recalculate_delete_dates_for_user(self, user_id, default_days=30):
        """
        For the given user, look at priv_cats, build:
            category_name -> days_until_delete
        Then for each email, set delete_date = collected_date + days_for_that_category
        (or default_days if category is missing).
        """
        # 1) Get category config from priv_cats
        query_cats = 'SELECT priv_cats FROM public.user_data WHERE user_id = %s'
        cat_rows = self.conn._get(query_cats, (user_id,))
        cat_days = {}

        if cat_rows and cat_rows != DB_CONST.DB_ERROR:
            raw_cats = cat_rows[0][0]
            cats = None

            if raw_cats:
                if isinstance(raw_cats, str):
                    try:
                        cats = json.loads(raw_cats)
                    except Exception:
                        cats = None
                else:
                    # If psycopg2 already decoded jsonb into Python
                    cats = raw_cats

            if isinstance(cats, list):
                for c in cats:
                    if not isinstance(c, dict):
                        continue
                    name = c.get("name")
                    days = c.get("days_until_delete")
                    if name and isinstance(days, int):
                        cat_days[name] = days

        # 2) Fetch this user's emails: id, category, collected_date
        query_emails = '''
            SELECT id, category, collected_date
            FROM public.email_data
            WHERE user_id = %s
        '''
        email_rows = self.conn._get(query_emails, (user_id,))
        if not email_rows or email_rows == DB_CONST.DB_ERROR:
            return

        update_query = 'UPDATE public.email_data SET delete_date = %s WHERE id = %s'

        for email_id, category, collected_date in email_rows:
            # Decide how many days to keep this email
            days = cat_days.get(category, default_days)

            base_dt = collected_date or dt.now(tz.utc)
            if base_dt.tzinfo is None:
                base_dt = base_dt.replace(tzinfo=tz.utc)

            new_delete = base_dt + timedelta(days=days)
            self.conn._set(update_query, (new_delete, email_id))
