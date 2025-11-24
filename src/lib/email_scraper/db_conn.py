# Matt 4:4

import psycopg2 as pg
# from src.lib.email_scraper.email_consts import DB_Const
from email_consts import DB_Const, EMAIL_CONST
from datetime import datetime as dt
from datetime import timezone as tz

class DB_Connection:
    
    def _check_pass(conn, user_id, password):
        query = 'SELECT user_pass FROM public.user_data WHERE user_id = %s'
        cur = conn.cursor()
        try:
            cur.execute(query, (user_id,))
            check = cur.fetchall()
            print(check)

            if check is None:
                return EMAIL_CONST.MISSING_ACCOUNT
            elif check == password:
                return EMAIL_CONST.LOGIN_SUCCESS
            else:
                return EMAIL_CONST.INCORRECT_ACCOUNT_INFO
        except:
            print('User error')
        
        return DB_Const.DB_ERROR
    
    def _add_email_data(conn, data):
        '''
        The param data should ideally be a single tuple or 1D array
        '''
        # Maybe format into tuple before
        query = '''INSERT INTO public.email_data (user_id, sender_id, category, data, delete_date) 
        VALUES (%s, %s, %s, %s, %s)'''
        cur = conn.cursor()
        try:
            cur.execute(query, (data,))
            conn.commit()
        except:
            print('Unable to write data')

    def _delete_old_emails(conn):
        now = dt.now(tz.utc)
        query = 'DELETE FROM public.email_data WHERE delete_date < %s'
        cur = conn.cursor()
        try:
            cur.execute(query, (now,))
            conn.commit()
            now.astimezone()
            print(f'All emails past {now.strftime('%m/%d/%Y')} have been deleted.')
        except:
            print('Email delete error')

    def _test_connection():
        '''
        Tests connection with 
        '''
        conn = None
        try:
            conn = pg.connect(
                database = DB_Const.PG_DB,
                user = DB_Const.PG_USER,
                password = DB_Const.PG_PASS,
                host = DB_Const.PG_HOST,
                port = DB_Const.PG_PORT
            )
        except:
            print('Database connection error.')
        return conn
    
    def _gather_data_by_user(conn, user_id):
        '''
        This functions uses SQL to gather all emails by user_id.
        Ensure in previous function that user_id == login id
        '''
        query = 'SELECT * FROM public.email_data WHERE user_id = %s'
        cur = conn.cursor()
        cur.execute(query, (user_id,))
        data = cur.fetchall()
        return [list(t) for t in data]

    def _gather_data_by_sender(conn, user_id, sender_id):
        '''
        This functions uses SQL to gather all emails by sender.
        Ensure in previous function that user_id == login id
        '''
        query = 'SELECT * FROM public.email_data WHERE user_id = %s AND sender_id = %s'
        cur = conn.cursor()
        cur.execute(query, (user_id, sender_id,))
        data = cur.fetchall()
        return [list(t) for t in data]

    def _gather_data_by_category(conn, category):
        '''
        This functions uses SQL to gather all emails by category.
        Ensure in previous function that user_id == login id for private categories
        '''
        query = 'SELECT * FROM public.email_data WHERE category = %s'
        cur = conn.cursor()
        cur.execute(query, (category,))
        data = cur.fetchall()
        return [list(t) for t in data]


if __name__ == '__main__':
    cursor = DB_Connection._test_connection()
    cursor.execute('SELECT * FROM public.email_data')
    print(cursor.fetchall())