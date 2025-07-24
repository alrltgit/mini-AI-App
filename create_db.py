import sqlite3

def create_database():
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    cursor.execute("create table data (ID INTEGER PRIMARY KEY AUTOINCREMENT, PROMPT TEXT, REPLY TEXT, DATE DATE)")
    connection.close()



