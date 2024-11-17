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


class CartItem(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship('Product', backref='cart_items')
    user = db.relationship('User', backref='cart_items')


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


@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing!'}), 401

    try:
        token = token.split(' ')[1]
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = decoded_token['user_id']
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401

    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    if not product_id:
        return jsonify({'message': 'Product ID is required'}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404

    cart_item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)

    db.session.commit()
    return jsonify({'message': 'Product added to cart'}), 200


@app.route('/cart/remove', methods=['DELETE'])
def remove_from_cart():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing!'}), 401

    try:
        token = token.split(' ')[1]
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = decoded_token['user_id']
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401

    data = request.get_json()
    product_id = data.get('product_id')

    if not product_id:
        return jsonify({'message': 'Product ID is required'}), 400

    cart_item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
    if not cart_item:
        return jsonify({'message': 'Product not found in cart'}), 404

    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({'message': 'Product removed from cart'}), 200


@app.route('/cart/update_quantity', methods=['PUT'])
def update_quantity():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing!'}), 401

    try:
        token = token.split(' ')[1]
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = decoded_token['user_id']
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401

    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    if not product_id or quantity is None:
        return jsonify({'message': 'Product ID and quantity are required'}), 400

    cart_item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
    if not cart_item:
        return jsonify({'message': 'Product not found in cart'}), 404

    if quantity <= 0:
        db.session.delete(cart_item)
    else:
        cart_item.quantity = quantity

    db.session.commit()
    return jsonify({'message': 'Quantity updated successfully'}), 200


@app.route('/cart', methods=['GET'])
def view_cart():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing!'}), 401

    try:
        token = token.split(' ')[1]
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = decoded_token['user_id']
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401

    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    cart_details = [
        {
            'id': item.id,
            'product_id': item.product.id,
            'name': item.product.name,
            'price': str(item.product.price),
            'image_url': item.product.image_url,
            'quantity': item.quantity,
        } for item in cart_items
    ]
    total_price = sum(float(item['price']) * item['quantity'] for item in cart_details)

    return jsonify({'cart': cart_details, 'total_price': str(total_price)}), 200


@app.route('/cart/count', methods=['GET'])
def cart_count():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'count': 0}), 200  # Puste koszyki dla niezalogowanych

    try:
        token = token.split(' ')[1]
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = decoded_token['user_id']
    except jwt.ExpiredSignatureError:
        return jsonify({'count': 0}), 200
    except jwt.InvalidTokenError:
        return jsonify({'count': 0}), 200

    count = db.session.query(db.func.sum(CartItem.quantity)).filter_by(user_id=user_id).scalar() or 0
    return jsonify({'count': count}), 200


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
