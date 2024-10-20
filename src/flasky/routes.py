from flask import Flask, request, render_template, url_for, redirect, session, flash
from flask_cors import cross_origin, CORS
from src.datahandler.dbClasses import UserHandler

app = Flask(__name__)
CORS(app)

userHandler = UserHandler()


@app.route('/')
def index():
    if session.get('user_id'):
        return render_template
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get("email")
        password = request.form.get("password")
        user = userHandler.get_user(email=email, password=password)
        if user:
            session['user_id'] = user['user_id']
            return redirect(url_for("index"))
        else:
            flash("Email or password did not match")
            return redirect(url_for('login'))
