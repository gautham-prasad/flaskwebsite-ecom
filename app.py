import os
from flask import Flask, jsonify, request, url_for
from flask_mail import Mail, Message
from flask_login import LoginManager, login_user, current_user, logout_user
from itsdangerous.exc import BadTimeSignature, SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from models import *                             

app = Flask(__name__)

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(id):
    return users.query.get(int(id))

app.config['SECRET_KEY'] = 'secret'
# os.environ.get('SECRET')
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://mmfxgxyvvqhulu:8aeaf8e8265a39c7fa812f9f9950d46812c384bb4a481b64e647325b6eb9c2de@ec2-54-156-60-12.compute-1.amazonaws.com:5432/de40f3aaq2g93o'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ywrhztcgyxonjq:4fc3b8bff68944225f9c337fe4878d2af98803bd020c2e9ec15710ef38d5c051@ec2-54-211-160-34.compute-1.amazonaws.com:5432/d117o9pe0b26u0'
db = SQLAlchemy(app)

sender_email = 'gauthampg1203@gmail.com'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = sender_email
app.config['MAIL_PASSWORD'] = 'quwqaoleljpvqitr'
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
        return jsonify({'msg': msg, 'username': username, 'email': email, 'password': password, 'uuid':token})

    elif request.json == 'POST':
        msg = 'Please fill out the form!'
        return jsonify({'msg': msg})

    return jsonify({'msg': "redirect to register page"})

@app.route("/verify/<token>", methods=['GET'])
def verify(token):
    try:
        email = serializer.loads(token,max_age=60)

    except SignatureExpired:
        msg = 'Token expired!'
        return jsonify({'msg': msg})
        
    except BadTimeSignature:
        msg = 'Token timed out!'
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
                login_user(user_name)
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