from .sql_pool import SQLiteConnectionPool
import os

THIS_DIR = os.path.dirname(__file__)

ENGINE = SQLiteConnectionPool(2, os.path.join(THIS_DIR, '..','Data','Data.db'))

class Users:
    def __init__(self, connection):

        self.connection = connection
        cur = self.connection.cursor()
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS Users (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
                Email TEXT,
                PassWord TEXT
            )'''
        )

    def addData(self, name:str, email:str, password:str):

        cur = self.connection.cursor()
        sql_update_query = """INSERT INTO Users (
            Name,
            Email,
            PassWord
        ) VALUES (?, ?, ?)"""
        cur.execute(sql_update_query, (name, email, password,))
        self.connection.commit()

        return


    def getdData(self):

        cur = self.connection.cursor()
        sql_get_query = """SELECT * FROM Users"""
        cur.execute(sql_get_query)
        rows = cur.fetchall()
    
   
        return rows
