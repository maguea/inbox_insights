# Matt 4:4

import psycopg2 as pg
#from src.lib.email_scraper.email_consts import DB_Const
from email_consts import DB_Const
from datetime import datetime as dt
from datetime import timezone as tz

class DB_Connection:

    def _adapter(data):
        '''
        Change to format into the following format:
        'id' = int (see opcode breakdown)
        'user_id' = string (username),
        'sender_id' = string (sender email address),
        'category' = string (add '-' in the beginning for private),
        'data' : text (long string) email body/summary,
        'collected_date' : datetime (collected date, will default to now, UTC),
        'delete_date' : datetime (delete date)
        '''
        adapted = {
            'id': None,
            'user_id': None,
            'sender_id' : None,
            'category' : None,
            'data' : None,
            'collected_date' : None,
            'delete_date' : None
        }
        return adapted

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
        print(data) # Test format

    def _gather_data_by_sender(conn, user_id, sender_id):
        '''
        This functions uses SQL to gather all emails by sender.
        Ensure in previous function that user_id == login id
        '''
        query = 'SELECT * FROM public.email_data WHERE user_id = %s AND sender_id = %s'
        cur = conn.cursor()
        cur.execute(query, (user_id, sender_id,))
        data = cur.fetchall()
        print(data) # Test format

    def _gather_data_by_category(conn, category):
        '''
        This functions uses SQL to gather all emails by category.
        Ensure in previous function that user_id == login id for private categories
        '''
        query = 'SELECT * FROM public.email_data WHERE category = %s'
        cur = conn.cursor()
        cur.execute(query, (category,))
        data = cur.fetchall()
        print(data) # Test format


if __name__ == '__main__':
    cursor = DB_Connection._test_connection()
    cursor.execute('SELECT * FROM public.email_data')
    print(cursor.fetchall())

