import sqlite3
from sqlite3 import Error
from operator import itemgetter



class Database:
    def __init__(self,path):
        # create a database connection
        self.conn = self.create_connection(path)

        # create tables
        if self.conn is not None:
            # create projects table
            self.create_rolls_table()
        else:
            print("Error! cannot create the database connection.")


    def create_connection(self,db_file):
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
            return self.conn
        except Error as e:
            print(e)

        return self.conn


    def create_rolls_table(self):
        sql_create_rolls_table = """CREATE TABLE IF NOT EXISTS roll (
                                        id integer PRIMARY KEY,
                                        roll_session_id TEXT NOT NULL,
                                        die_one_result INTEGER NOT NULL,
                                        die_two_result INTEGER NOT NULL,
                                        date_time_roll TEXT NOT NULL
                                    );"""
        try:
            c = self.conn.cursor()
            c.execute(sql_create_rolls_table)
        except Error as e:
            print(e)


    def add_roll(self,roll):
        sql = f''' INSERT INTO roll(roll_session_id,die_one_result,die_two_result,date_time_roll)
                VALUES('{roll['roll_session_id']}',{roll['die_one_result']},'{roll['die_two_result']}','{roll['date_time_roll']}') '''
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()
        return cur.lastrowid

    def get_roll_sessions(self):
        sql = 'select roll_session_id,  MIN(date_time_roll), MAX(date_time_roll), COUNT(roll_session_id) FROM roll GROUP BY roll_session_id'
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        sessions = [{
            'roll_session_id' : r[0],
            'start_time' : r[1],
            'end_time' : r[2],
            'rolls' : r[3]
        } for r in rows]
        return sessions

    def get_rolls(self, roll_id,no_of_rolls):
        sql2 = f''' SELECT COUNT(die_one_result + die_two_result) as total12 
            FROM roll  
            WHERE roll_session_id = '{roll_id}' 
            AND die_one_result + die_two_result = 2 '''
        sql3 = f''' SELECT COUNT(die_one_result + die_two_result) as total12 
            FROM roll  
            WHERE roll_session_id = '{roll_id}' 
            AND die_one_result + die_two_result = 3 '''
        sql4 = f''' SELECT COUNT(die_one_result + die_two_result) as total12 
            FROM roll  
            WHERE roll_session_id = '{roll_id}' 
            AND die_one_result + die_two_result = 4 '''
        sql5 = f''' SELECT COUNT(die_one_result + die_two_result) as total12 
            FROM roll  
            WHERE roll_session_id = '{roll_id}' 
            AND die_one_result + die_two_result = 5 '''
        sql6 = f''' SELECT COUNT(die_one_result + die_two_result) as total12 
            FROM roll  
            WHERE roll_session_id = '{roll_id}' 
            AND die_one_result + die_two_result = 6 '''
        sql7 = f''' SELECT COUNT(die_one_result + die_two_result) as total12 
            FROM roll  
            WHERE roll_session_id = '{roll_id}' 
            AND die_one_result + die_two_result = 7 '''
        sql8 = f''' SELECT COUNT(die_one_result + die_two_result) as total12 
            FROM roll  
            WHERE roll_session_id = '{roll_id}' 
            AND die_one_result + die_two_result = 8 '''
        sql9 = f''' SELECT COUNT(die_one_result + die_two_result) as total12 
            FROM roll  
            WHERE roll_session_id = '{roll_id}' 
            AND die_one_result + die_two_result = 9 '''
        sql10 = f''' SELECT COUNT(die_one_result + die_two_result) as total12 
            FROM roll  
            WHERE roll_session_id = '{roll_id}' 
            AND die_one_result + die_two_result = 10 '''
        sql11 = f''' SELECT COUNT(die_one_result + die_two_result) as total12 
            FROM roll  
            WHERE roll_session_id = '{roll_id}' 
            AND die_one_result + die_two_result = 11 '''
        sql12 = f''' SELECT COUNT(die_one_result + die_two_result) as total12 
            FROM roll  
            WHERE roll_session_id = '{roll_id}' 
            AND die_one_result + die_two_result = 12 '''
        # sql9 = f''' SELECT COUNT(die_one_result + die_two_result) as total12 
        #     FROM roll  
        #     WHERE roll_session_id = '{roll_id}' 
        #     AND die_one_result + die_two_result = 5 '''
        print('Number of Rolls', no_of_rolls, '\n')
        rolls = {}
        for i in range(2,13):
            sql = f''' SELECT COUNT(die_one_result + die_two_result) as total 
            FROM roll  
            WHERE roll_session_id = '{roll_id}' 
            AND die_one_result + die_two_result = {i} '''
            cur = self.conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            rolls[i] = { 'rolls' : rows[0][0], 'percent' : round((100 / rows[0][0]) * 100,2) }
        #rolls_sorted = rolls.sort(rolls, key=itemgetter('percent')) 
        return rolls

