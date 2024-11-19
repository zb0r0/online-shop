from functools import wraps
from flask import request, jsonify
import jwt
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from app import app, db


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            token = token.split(" ")[1]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            user = User.query.get(data['user_id'])
            if not user or user.permissions != 1:
                return jsonify({'message': 'Admin permissions required!'}), 403
        except Exception:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(*args, **kwargs)
    return decorated_function


def generate_token(user_id):
    expiration = datetime.utcnow() + timedelta(hours=1)
    token = jwt.encode({'user_id': user_id, 'exp': expiration}, app.config['SECRET_KEY'], algorithm='HS256')
    return token


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    required_fields = ['username', 'password', 'permissions', 'birthdate', 'gender', 'location']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing data'}), 400

    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    birthdate = datetime.strptime(data['birthdate'], '%Y-%m-%d').date()

    new_user = User(
        username=data['username'],
        password=hashed_password,
        permissions=data['permissions'],
        birthdate=data['birthdate'],
        gender=data['gender'],
        location=data['location']
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if user and check_password_hash(user.password, data['password']):
        token = generate_token(user.id)
        print(f"User {user.username} logged in with permissions: {user.permissions}")
        return jsonify({'message': 'Login successful', 'token': token}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401


@app.route('/check_login', methods=['GET'])
def check_login():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({'message': 'Missing token'}), 401

    try:
        token = token.split(' ')[1]
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = decoded_token['user_id']
        user = User.query.get(user_id)

        if user:
            print(f"Checked login for user: {user.username}, permissions: {user.permissions}")
            return jsonify({'message': f'Welcome back, {user.username}, permissions: {user.permissions}'}), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401
