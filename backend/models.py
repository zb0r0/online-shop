from datetime import datetime
from app import db
from sqlalchemy import ForeignKey


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

    sales = db.relationship('Sale', back_populates='product')

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


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    zip_code = db.Column(db.String(5), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(9), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=True, default='SUCCESS')
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref='orders')

    def __repr__(self):
        return f'<Order {self.id}>'



class OrderProduct(db.Model):
    __tablename__ = 'order_products'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    order = db.relationship('Order', back_populates='products')
    product = db.relationship('Product', back_populates='orders')
    sales = db.relationship('Sale', back_populates='order_product', cascade="all, delete")

    Order.products = db.relationship('OrderProduct', back_populates='order')
    Product.orders = db.relationship('OrderProduct', back_populates='product')


class Sale(db.Model):
    __tablename__ = 'sales'

    id = db.Column(db.Integer, primary_key=True)
    order_product_id = db.Column(db.Integer, db.ForeignKey('order_products.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_per_unit = db.Column(db.Numeric(10, 2), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    sold_at = db.Column(db.DateTime, default=datetime.utcnow)

    order_product = db.relationship('OrderProduct', back_populates='sales')
    product = db.relationship('Product', back_populates='sales')

    def __repr__(self):
        return f'<Sale {self.id}>'
