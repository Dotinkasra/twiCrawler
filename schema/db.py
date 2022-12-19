import sqlite3

class DB():
    def __init__(self, dbname: str = 'twidouga.db') -> None:
        self.dba = DBaccess(dbname)

    def insert_single_url(self, url: str):
        if not url:
            return
        self.dba.insert(
            '''
            INSERT INTO 
            url_records (url) VALUES (?);
            ''', (url,), "url_records"
        )

    def check_url_exists(self, url: str) -> bool:
        result = self.dba.select(
            '''
            SELECT count(*)
            FROM url_records
            WHERE url = ?;
            ''', (url,)
        )
        if result[0][0] > 0:
            return True
        return False

class DBaccess():
    def __init__(self, dbname) -> None:
        self.dbname = dbname

        # SQLiteデータベースに接続
        conn = sqlite3.connect(self.dbname)

        # cursorオブジェクトを作成
        cursor = conn.cursor()

        # テーブルを作成するSQL文を実行
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS url_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT UNIQUE NOT NULL,
        created_at DATETIME DEFAULT (datetime('now', 'localtime'))
        );
        ''')

        # 変更をコミット
        conn.commit()

        # 接続を閉じる
        conn.close()

    def close(self):
        self.conn.close()

    def connect(self):
        self.conn = sqlite3.connect(self.dbname)
        self.cur = self.conn.cursor()

    def select(self, sql: str, parameta: tuple = None) -> list:
        self.connect()
        if parameta:
            self.cur.execute(sql, parameta)
        else:
            self.cur.execute(sql)
        result = self.cur.fetchall()
        self.close()
        return result

    def insert(self, sql: str, parameta: tuple = None, table_name: str = None) -> None|list:
        self.connect()
        if parameta:
            self.cur.execute(sql, parameta)
        else:
            self.cur.execute(sql)
        self.conn.commit()

        result = None
        if table_name:
            self.cur.execute(f"SELECT * FROM {table_name} WHERE rowid = last_insert_rowid();")
            result = self.cur.fetchall()
        self.close()
        return result

    def delete(self, sql: str, parameta: tuple = None):
        self.connect()
        if parameta:
            self.cur.execute(sql, parameta)
        else:
            self.cur.execute(sql)
        self.conn.commit()
        self.close()