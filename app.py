import os, psycopg2
import re
from flask import Flask, jsonify, request, url_for
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager, login_user, login_required, logout_user, current_user       
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, BadTimeSignature, SignatureExpired
from models import Tempusers, Users, db
app = Flask(__name__)
CORS(app)

DATABASE_URL = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

db.init_app(app)

app.config['SECRET_KEY'] = os.environ.get('SECRET')
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

sender_email = os.environ.get('SENDER_EMAIL')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = sender_email
app.config['MAIL_PASSWORD'] = os.environ.get('SENDER_PASSWORD')
mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return Users.query.filter_by(id = id).first()

@app.login_manager.unauthorized_handler
def unauth_handler():
    msg = 'login to access this page'
    return jsonify({'msg': msg}), 401

@app.route("/register", methods=['GET', 'POST'])
def register():

    if request.method == 'POST' and 'username' in request.json and 'email' in request.json and 'password' in request.json:  
        email = request.json['email']
        username = request.json['username']
        password = generate_password_hash(request.json['password'], method='sha256')

        user = Users.query.filter_by(email=email).first()

        if user is not None:

            if user.email == email:
                msg = 'Account exist for %s' % email 
                return jsonify({'msg': msg}), 401

            elif user.username == username:
                msg = 'username taken!'
                return jsonify({'msg': msg}), 401

        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
            return jsonify({'msg': msg}), 401

        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only alphabets and numbers!'
            return jsonify({'msg': msg}), 401

        
        token = serializer.dumps(email)
        link = url_for('verify',token=token,_external=True)
        msg = Message('Verification link',sender=('Gautham','sender_email'),recipients=[email, sender_email])
        msg.body = 'Congratulations! Your link is {}'.format(link)
        
        tempuser = Tempusers(email = email, username =username, password = password)
        db.session.add(tempuser)
        db.session.commit()

        mail.send(msg)

        msg = "Please verify email to complete registration"
        return jsonify({'msg': msg, 'username': username, 'email': email, 'password': password, 'token':token})

    elif request.json == 'POST':
        msg = 'Please fill out the form!'
        return jsonify({'msg': msg}), 401

    return jsonify({'msg': "redirect to register page"}), 302

@app.route("/verify/<token>", methods=['GET'])
def verify(token):
    
    try:
        email = serializer.loads(token, max_age = 300)
        temp_user = Tempusers.query.filter_by(email= email).first()
    
    except SignatureExpired:
        msg = 'Token Timed Out!'
        return jsonify({'msg':msg}), 401

    except BadTimeSignature:
        msg = 'Invalid Token!'
        return jsonify({'msg':msg}), 401

    if temp_user.verified == False:

        temp_user.verified = True
        db.session.commit()

        if email == temp_user.email:

            user = Users(email = temp_user.email, username = temp_user.username, password = temp_user.password)
            db.session.add(user)
            db.session.commit()

            msg = 'Registration successful!'
            return jsonify({'msg':msg, 'email': email, 'redirect':'registration page'})

    msg = 'Your account is verified, login to continue'
    return jsonify({'msg':msg})

@app.route("/login", methods=['GET','POST'])
def login():

    if request.method == 'POST' and 'email' in request.json and 'password' in request.json:
        email = request.json['email']
        user = Users.query.filter_by(email=email).first()

        if user is None or email != user.email:
            msg = 'Invalid email or password'
            return jsonify({'msg': msg}), 401
    
        user_password = check_password_hash(user.password,request.json['password'])

        if user_password is False:
            msg = 'Invalid email or password'
            return jsonify({'msg': msg}), 401
        
        login_user(user)
        print('Login successful')
        msg = 'Welcome back, %s' % current_user.email
        return jsonify({'msg': msg})

    elif request.json == 'POST': 
        msg = 'Please fill out the form!'
        return jsonify({'msg': msg}), 401

    msg = 'Redirect to login page'
    return jsonify({'msg': msg}), 302

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    
    user = current_user.username
    logout_user()
    msg = 'logged out %s' % user
    return jsonify({'msg': msg}), 200

@app.route("/home", methods=['GET'])
@login_required
def home():
    msg = 'current user is, %s' %current_user.username 
    return jsonify({'msg': msg}), 200

if __name__ == '__main__':
    app.run()