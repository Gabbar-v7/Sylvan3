from flask import Flask, request, render_template, url_for, redirect, session
from flask_cors import cross_origin, CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    if session.get('user_id'):
        return render_template
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('base.html')
    else:
        return "Not Done Yet"
