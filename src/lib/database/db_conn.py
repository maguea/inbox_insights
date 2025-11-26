# Matt 4:4
import psycopg2 as pg
from src.lib import DB_CONST


class DB_Connection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_conn()
        return cls._instance

    def _init_conn(self):
        try:
            self.conn = pg.connect(
                database=DB_CONST.PG_DB,
                user=DB_CONST.PG_USER,
                password=DB_CONST.PG_PASS,
                host=DB_CONST.PG_HOST,
                port=DB_CONST.PG_PORT,
            )
        except Exception as e:
            print("Database connection error:", e)
            self.conn = None
    
    def _test_connection(self):
        '''
        Tests connection to the database. returns connection instance 
        '''
        try:
            self.conn = pg.connect(
                database = DB_CONST.PG_DB,
                user = DB_CONST.PG_USER,
                password = DB_CONST.PG_PASS,
                host = DB_CONST.PG_HOST,
                port = DB_CONST.PG_PORT
            )
        except:
            print('Database connection error.')
        return self.conn
    
    def _set(self, query, args):
        '''
        Make a change to the database. will return DB_CONST.DB_ERROR if error
        
        :param query: the query prompt
        :param args: the arguments for the query in a tuple
        '''
        cur = self.conn.cursor()
        try:
            cur.execute(query, (args,))
            self.conn.commit()
        except:
            print('DB Commit Error')
            return DB_CONST.DB_ERROR
        
    def _get(self, query, args):
        '''
        Return data from the database. will return DB_CONST.DB_ERROR if error
        
        :param query: the query prompt
        :param args: the arguments for the query in a tuple
        '''
        cur = self.conn.cursor()
        try:
            cur.execute(query, (args,))
            data = cur.fetchall()
            return data
        except:
            print('DB Fetch Error')
            return DB_CONST.DB_ERROR
    

if __name__ == '__main__':
    cursor = DB_Connection._test_connection()
    cursor.execute('SELECT * FROM public.email_data')
    print(cursor.fetchall())