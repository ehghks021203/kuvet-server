from config.default import *
import os
import pymysql

HOST = os.getenv("DB_HOST", "default-host")
USER = os.getenv("DB_USER", "default-user")
PASSWORD = os.getenv("DB_PASSWORD", "default-password")
NAME = os.getenv("DB_NAME", "default-db")

class Database:
    def __init__(self):
        self.db = pymysql.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            db=NAME,
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    def execute(self, query, args={}):
        self.cursor.execute(query, args)

    def executeOne(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        return row

    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.db.commit()

    def close(self):
        self.cursor.close()
        self.db.close()