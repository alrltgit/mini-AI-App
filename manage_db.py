from flask import g
import sqlite3

def create_database():
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    cursor.execute("create table data (ID INTEGER PRIMARY KEY AUTOINCREMENT, PROMPT TEXT, REPLY TEXT)")
    connection.close()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('data.db')
    return db