import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()
cursor.execute("create table data (ID INTEGER PRIMARY KEY AUTOINCREMENT, PROMPT TEXT, REPLY TEXT, DATE DATE)")


connection.close()



