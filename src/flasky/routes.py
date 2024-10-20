from flask import Flask, request, render_template, url_for, redirect, session, flash
from flask_cors import cross_origin, CORS
from src.datahandler.dbClasses import UserHandler
from keys import FLASK_SESSION_KEY

app = Flask(__name__)
app.secret_key = FLASK_SESSION_KEY
CORS(app)

userHandler = UserHandler()


@app.route('/')
def index():
    if session.get('user_id'):
        flash('Changes have been saved successfully!', 'success')
        flash('You have 3 new messages in your inbox.', 'info')
        flash('Don\'t forget to save your data.', 'warning')
        flash('The server is not respoasdanding, try again later.', 'danger')
        return render_template('components/flash_card.html')
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
        if user and email and password:
            session['user_id'] = user[0]['user_id']
            return redirect(url_for("index"))
        else:
            flash("Email or password did not match")
            return redirect(url_for('login'))


@app.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        flash('Changes have been saved successfully!', 'success')
        flash('You have 3 new messages in your inbox.', 'info')
        flash('Don\'t forget to save your data.', 'warning')
        flash('The server is not respoasdanding, try again later.', 'danger')
        return render_template('sign_up.html')
    else:
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        password = request.form.get('password')
        if not (name and phone and email and password):
            flash("Fields cannot be empty")
            return redirect(url_for('signup'))
        elif userHandler.new_user(name, email, phone, password):
            session['user_id'] = userHandler.get_user(email=email, phone=phone)
            return redirect(url_for('index'))
        else:
            flash("Email or phone already exists")
            return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


userHandler.new_user("Gabbar", "asd@gmail.com", "912771811", "asd", )
