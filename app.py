from flask import Flask, redirect, url_for, request, render_template, g, session
from google import genai
from utils import send_api_request, add_data_to_database, create_session
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
client = genai.Client()
app.secret_key = os.environ.get('SESSION_SECRET_KEY')
@app.route('/')
def index():
    chat = session.get('chat', [])
    return render_template('index.html', chat=chat)

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form['prompt']
    response = send_api_request(prompt, client)
    add_data_to_database(prompt, response)
    create_session(prompt, response)
    return redirect(url_for('index'))
@app.route('/clear', methods=['POST'])
def clear():
    session.pop('chat', None)
    return redirect(url_for('index'))

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(debug=True)
