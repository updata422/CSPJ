from flask import Flask, Blueprint, render_template, make_response, request, flash, jsonify
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
import re
import uuid
from flask_recaptcha import ReCaptcha

auth = Blueprint('auth', __name__)
app = Flask(__name__)
recaptcha = ReCaptcha(app=app)

app.config.update(dict(
    RECAPTCHA_ENABLED = True,
    RECAPTCHA_SITE_KEY = "6LeR6oIbAAAAAHsAh_-_l-BlfrDHaK-1icttf8nq",
    RECAPTCHA_SECRET_KEY = "6LeR6oIbAAAAAE-A9QHfJNnfJa-EI1CgHT0t25Jk",
))

recaptcha = ReCaptcha()
recaptcha.init_app(app)

@auth.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()

    #if not recaptcha.verify():
        #return make_response(jsonify({'message': 'Please verify captcha'}), 401)

    if user:
        if not check_password_hash(user.password, password):
            return make_response(jsonify({'message': 'Email/Password incorrect.', 'userid': uuid.uuid1()}), 401)    # Fake a GUID

        return make_response(jsonify({'message': 'Email/Password Incorrect', 'user_id': user.typing_id}), 401)
        #return make_response(jsonify({'message': 'Login successful', 'user_id': user.typing_id}), 200)
    else:
        return make_response(jsonify({'message': 'Email/Password Incorrect', 'userid': uuid.uuid1()}), 401)         # Fake a GUID


@auth.route('/api/sign-up', methods=['POST'])
def api_sign_up():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    # Email validation
    if user or len(email) < 4:
        return make_response(jsonify({'message': 'Sign up form invalid.'}), 401)
    elif not re.search("@", email):
        return make_response(jsonify({'message': 'Invalid email!'}), 401)

    # Password validation
    elif len(password) < 7:
        return make_response(jsonify({'message': 'Password too short!'}), 401)
    elif not re.search("[a-z]", password):
        return make_response(jsonify({'message': 'Password needs to contain at least a lowercase alphabet!'}), 401)
    elif not re.search("[A-Z]", password):
        return make_response(jsonify({'message': 'Password needs to contain at least an uppercase alphabet!'}), 401)
    elif not re.search("[0-9]", password):
        return make_response(jsonify({'message': 'Password needs to contain at least a number!'}), 401)
    elif not re.search("[_@$]", password):
        return make_response(jsonify({'message': 'Password needs to contain at least one of the following special characters: _,@,$'}), 401)

    else:
        new_user = User(email=email, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({'message': 'New user created.', 'user_id': new_user.typing_id}), 201)


@auth.route('/login')
def login():
    return render_template("login.html")


@auth.route('/sign-up')
def sign_up():
    return render_template("sign_up.html")

@auth.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    user_email = data.get('email')
    user_password = data.get('password')

    user = db.session.execute(f"SELECT * FROM User WHERE email = '{user_email}' AND password = '{user_password}'").first()
    uName = getRequestString("username");
    uPass = getRequestString("userpassword");

    sql = 'SELECT * FROM Users WHERE Name ="' + uName + '" AND Pass ="' + uPass + '"'


    if user:
        return make_response(jsonify({'message': 'Login succesful'}), 200)

    else:
        if User.query.filter_by(email=user_email).first():
            return make_response(jsonify({'message': 'Password incorrect.'}), 401)

        elif User.query.filter_by(password=user_password).first():
            return make_response(jsonify({'message': 'No user with that email.'}), 401)

        else:
            return make_response(jsonify({'message': 'No user with that email and password'}), 401)


@auth.route('/api/sign-up', methods=['POST'])
def api_sign_up():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user or len(email) < 4:
        return make_response(jsonify({'message': 'Sign up form invalid.'}), 401)
    else:
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({'message': 'New user created.'}), 201)


@auth.route('/login')
def login():
    return render_template("login.html")


@auth.route('/sign-up')
def sign_up():
    return render_template("sign_up.html")

