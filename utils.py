from flask import session
from google.genai import errors
import os
from manage_db import create_database, get_db

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Gets the current file's directory
DB_PATH = os.path.join(BASE_DIR, 'data.db')

def send_api_request(prompt, client):
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
    except errors.APIError as e:
        response = f"Error: {e}"
    return response

def add_data_to_database(prompt, response):
    if not os.path.isfile(DB_PATH):
        create_database()
    db = get_db()
    db.execute('insert into data (PROMPT, REPLY) values (?,?)', (prompt, response.text))
    db.commit()

def create_session(prompt, response):
    if 'chat' not in session:
        session['chat'] = []
    session['chat'].append({'prompt': prompt, 'reply': response.text})
    session.modified = True