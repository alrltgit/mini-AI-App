from flask import Flask, request, render_template, g, session
from google import genai
from utils import send_api_request, add_data_to_database, create_session
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
    response = send_api_request(prompt, client)
    add_data_to_database(prompt, response)
    create_session(prompt, response)
    return render_template('index.html', chat = session['chat'])

@app.route('/clear', methods=['POST'])
def clear():
    session.pop('chat')
    return render_template('index.html')

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(debug=True)
