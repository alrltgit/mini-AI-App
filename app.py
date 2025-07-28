from flask import Flask, request, render_template, g
from google import genai
import sqlite3
from create_db import create_database
import os

app = Flask(__name__)
client = genai.Client()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form['prompt']
    response = client.models.generate_content(
        model = 'gemini-2.5-flash',
        contents = prompt
    )
    if not os.path.isfile('/Users/apple/PycharmProjects/mini-AI-App/data.db'):
        create_database()
    db = get_db()
    db.execute('insert into data (PROMPT, REPLY) values (?,?)', (prompt, response.text))
    db.commit()
    reply = response.text
    return render_template('response.html', response = reply)

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
