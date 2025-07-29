from flask import Flask, request, render_template, g, session
from google import genai
from google.genai import errors
import sqlite3
from create_db import create_database
import os
app = Flask(__name__)
client = genai.Client()
app.secret_key = os.environ.get('session_secret_key')
@app.route('/')
def index():
    session.clear()
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form['prompt']
    try:
        response = client.models.generate_content(
            model = 'gemini-2.5-flash',
            contents = prompt
        )
    except errors.APIError as e:
        response = f"Error: {e}"
    if not os.path.isfile('/Users/apple/PycharmProjects/mini-AI-App/data.db'):
        create_database()
    db = get_db()
    db.execute('insert into data (PROMPT, REPLY) values (?,?)', (prompt, response.text))
    db.commit()
    # print db
    # rows = db.execute('select * from data')
    # for row in rows:
    #    print (row)
    reply = response.text
    if 'chat' not in session:
        session['chat'] = []
    session['chat'].append({'prompt': prompt, 'reply': reply})
    session.modified = True
    return render_template('index.html', chat = session['chat'])

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('data.db')
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(debug=True)
