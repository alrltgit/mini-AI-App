from flask import Flask, request, render_template, g
from google import genai
import sqlite3

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
    db = get_db()
    # cursor = db.cursor()
    db.execute('insert into data (PROMPT, REPLY) values (?,?)', (prompt, response.text))
    db.commit()

    # print the db content
    rows = db.execute('select * from data')
    for row in rows:
        print (row)
    reply = response.text
    return render_template('response.html', response = reply)
    # return response.text

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
