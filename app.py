import os
import psycopg2
from models import tempusers, users, usersinfo                             
from flask import Flask, jsonify, request, url_for
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from itsdangerous.exc import BadTimeSignature, SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

app = Flask(__name__)


app.config['SECRET_KEY'] = os.environ.get('SECRET')
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

DATABASE_URL = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
db = SQLAlchemy(app)

sender_email = os.environ.get('SENDER_EMAIL')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = sender_email
app.config['MAIL_PASSWORD'] = os.environ.get('SENDER_PASSWORD')
mail = Mail(app)

@app.route("/register", methods=['GET', 'POST'])
def register():

    if request.method == 'POST' and 'username' in request.json and 'email' in request.json and 'password' in request.json:  
        email = request.json['email']
        username = request.json['username']
        password = generate_password_hash(request.json['password'], method='sha256')

        user_email = tempusers.query.filter_by(email=email).first()
        user_name = tempusers.query.filter_by(username=username).first()

        if user_email:
            msg = 'Account exist for %s' % email 
            return jsonify({'msg': msg})

        elif user_name:
            msg = 'username taken!'
            return jsonify({'msg': msg}) 
        
        token = serializer.dumps(email)
        link = url_for('verify',token=token,_external=True)
        msg = Message('Verification link',sender=('Gautham','sender_email'),recipients=[email])
        msg.body = 'Congratulations! Your link is {}'.format(link)
        mail.send(msg)
        
        tempuser = tempusers(email = email, username =username, password = password)
        db.session.add(tempuser)
        db.session.commit()

        msg = "Please verify email to complete registration"
        return jsonify({'msg': msg, 'username': username, 'email': email, 'password': password, 'token':token})

    elif request.json == 'POST':
        msg = 'Please fill out the form!'
        return jsonify({'msg': msg})

    return jsonify({'msg': "redirect to register page"})

@app.route("/verify/<token>", methods=['GET','POST'])
def verify(token):
    try:
        email = serializer.loads(token,max_age=120)

    except SignatureExpired:
        msg = 'Token expired!'
        return jsonify({'msg': msg})
        
    except BadTimeSignature:
        msg = 'Token seems incorrect!'
        return jsonify({'msg': msg})
    
    tempuser = tempusers.query.filter_by(email=email).first()

    user = users(email = email, username = tempuser.username)
    db.session.add(user)
    db.session.commit()

    userinfo = usersinfo(email = email, password = tempuser.password)
    db.session.add(userinfo)
    db.session.commit()

    msg = 'Congratulations, registration successful! Redirect to login page'
    return jsonify({'msg': msg, 'email':email})


@app.route("/", methods=['GET','POST'])
def login():

    if request.method == 'POST' and 'username' in request.json and 'password' in request.json:
        user_name = users.query.filter_by(username=request.json['username']).first()

        if user_name:
            user_password = usersinfo.query.filter_by(email=user_name.email).first()
            user_password = check_password_hash(user_password.password,request.json['password'])

            if user_password:
                msg = 'Welcome back, %s' % user_name.username
                return jsonify({'msg': msg})

            msg = 'Invalid username or password'
            return jsonify({'msg': msg})

        msg = 'Invalid username or password'
        return jsonify({'msg': msg})

    elif request.json == 'POST': 
        msg = 'Please fill out the form!'
        return jsonify({'msg': msg})

    msg = 'Redirect to login page'
    return jsonify({'msg': msg})

@app.route("/logout")
def logout():
    logout_user()
    msg = 'Logged out!'
    return jsonify({'msg': msg})

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    if not current_user.is_authenticated:
        msg = 'redirect to login page'
        return jsonify({'msg': msg})

    msg = 'Welcome to dashboard.'
    return jsonify({'msg': msg})

@app.route('/profile', methods=['GET', 'POST'])
def profile():

    if not current_user.is_authenticated:
        msg = 'redirect to login page'
        return jsonify({'msg': msg})

    msg = 'Welcome to profile.'
    return jsonify({'msg': msg})

if __name__ == '__main__':
    app.run()