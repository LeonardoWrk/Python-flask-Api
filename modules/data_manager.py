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

    def add_data(self, name:str, email:str, password:str):

        cur = self.connection.cursor()
        sql_update_query = """INSERT INTO Users (
            Name,
            Email,
            PassWord
        ) VALUES (?, ?, ?)"""
        cur.execute(sql_update_query, (name, email, password,))
        self.connection.commit()

        return


    def getd_data(self):

        cur = self.connection.cursor()
        sql_get_query = """SELECT * FROM Users"""
        cur.execute(sql_get_query)
        rows = cur.fetchall()

        return rows

    def verify_if_exist(self, name:str) -> bool:

        cur = self.connection.cursor()
        sql_check_query = """SELECT EXISTS(SELECT 1 FROM Users WHERE Email = ?)"""
        cur.execute(sql_check_query, (name,))
        result = cur.fetchone()[0]
        

        return result == 1


    def delete_data(self, name:str) -> bool:

        cur = self.connection.cursor()  
        sql_delete_query = """DELETE FROM Users WHERE Email = ?"""
        cur.execute(sql_delete_query, (name,))
        self.connection.commit()
        affected_rows = cur.rowcount

        return affected_rows > 0
    

    def update_data(self, current_email: str, name: str = None, email: str = None, password: str = None):
        cur = self.connection.cursor()
        sql_update_query = "UPDATE Users SET "
        params = []

        if name is not None:
            #+= para concatenar strings ou adicionar valores a variáveis numéricas.
            sql_update_query += "Name = ?, "
            params.append(name)
        if email is not None:
            sql_update_query += "Email = ?, "
            params.append(email)
        if password is not None:
            sql_update_query += "PassWord = ?, "
            params.append(password)
        
        # Remove a vírgula extra no final e adiciona a cláusula WHERE
        sql_update_query = sql_update_query.rstrip(', ') + " WHERE Email = ?"
        params.append(current_email)
        
        cur.execute(sql_update_query, tuple(params))
        self.connection.commit()
        affected_rows = cur.rowcount

        return affected_rows > 0
