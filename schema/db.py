from module.module import Modules
import pymysql.cursors
from dotenv import load_dotenv
from os.path import join, dirname
import os
import datetime

class DB():
    def __init__(self, dbname: str = 'url_records') -> None:
        self.dba = DBaccess(dbname)

    def insert_single_url(self, url: str):
        if not url:
            return
        
        video_id = Modules.extract_file_name_from_url(url)
        if not video_id:
            return
        
        now = datetime.datetime.now()
        
        self.dba.insert(
            sql =
            '''
            INSERT INTO 
            url_records (video_id, created_at, url) VALUES (%s, %s, %s);
            ''',
            parameta = (video_id, now, url,),
        )

    def check_url_exists(self, url: str) -> bool:
        if not url:
            return
        
        video_id = Modules.extract_file_name_from_url(url)
        if not video_id:
            return

        result = self.dba.select(
            '''
            SELECT count(*)
            FROM url_records
            WHERE video_id = %s;
            ''', (video_id,)
        )

        return True if result[0][0] > 0 else False

class DBaccess():
    def __init__(self, dbname) -> None:
        load_dotenv(verbose=True)
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)

        try:
            self.conn = pymysql.connect(
                host = os.environ.get("MARIADB_HOST"),
                user = os.environ.get('MARIADB_USER'),
                db = os.environ.get("MARIADB_DATABASE"),
                password = os.environ.get("MARIADB_PASSWORD"),
                charset="utf8mb4",
                cursorclass=pymysql.cursors.Cursor
            )

            self.table = dbname
        except Exception as e:
            print("close")
            print(e)
            self.conn.close()

    def select(self, sql: str, parameta: tuple = None) -> list:
        try:
            print("SELECT文")
            print(sql)
            with self.conn.cursor() as cursor:
                cursor.execute(sql, parameta)
                return cursor.fetchall()
        except Exception as e:
            print("close")
            print(e)
            self.conn.close()
        

    def insert(self, sql: str, parameta: tuple = None) -> None|list:
        try:
            print("INSERT文")
            print(sql)
            print(parameta)
            with self.conn.cursor() as cursor:
                cursor.execute(sql, parameta)
        except Exception as e:
            print("close")
            print(e)
            self.conn.close()

        try:
            self.conn.commit()
            print("コミット完了後SELECT")
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT last_insert_id() FROM url_records")
                return cursor.fetchall()
        except Exception as e:
            print("close")
            print(e)
            self.conn.close()
    
    def __del__(self):
        self.conn.close()
