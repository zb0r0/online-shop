import jwt
from datetime import timedelta
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_cors import CORS
from functools import wraps

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123123@localhost/sklep'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretKey:D'

db = SQLAlchemy(app)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            token = token.split(" ")[1]  # Extrahujemy token
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            user = User.query.get(data['user_id'])
            print('admin zalogowany xd')
            if not user or user.permissions != 1:
                return jsonify({'message': 'Admin permissions required!'}), 403
        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(*args, **kwargs)
    return decorated_function


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    category = db.Column(db.String(100))
    stock = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Dostępny')
    image_url = db.Column(db.String(255))
    tags = db.Column(db.ARRAY(db.String))
    gender = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<Product {self.name}>'


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    permissions = db.Column(db.Integer, nullable=False, check_constraint='permissions IN (0, 1)')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    birthdate = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    location = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


@app.route('/add_product', methods=['POST'])
@admin_required
def add_product():
    data = request.get_json()

    required_fields = ['name', 'price', 'description', 'category', 'gender']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing fields'}), 400

    new_product = Product(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        category=data['category'],
        stock=data.get('stock', 0),
        gender=data['gender'],
        image_url=data.get('image_url'),
        tags=data.get('tags', [])
    )

    db.session.add(new_product)
    db.session.commit()

    return jsonify({'message': 'Product added successfully'}), 201


@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.order_by(Product.stock.desc()).all()
    products_list = [
        {
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'stock': product.stock,
            'image_url': product.image_url
        }
        for product in products
    ]
    return jsonify(products_list), 200


def generate_token(user_id):
    expiration = datetime.utcnow() + timedelta(hours=1)  # Token wygasa po godzinie
    token = jwt.encode({'user_id': user_id, 'exp': expiration}, app.config['SECRET_KEY'], algorithm='HS256')
    return token


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    required_fields = ['username', 'password', 'permissions', 'birthdate', 'gender', 'location']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing data'}), 400

    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    try:
        birthdate = datetime.strptime(data['birthdate'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'message': 'Invalid birthdate format. Use YYYY-MM-DD.'}), 400

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


if __name__ == '__main__':
    app.run(debug=True)
