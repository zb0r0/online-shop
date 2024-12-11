from flask import request, jsonify
from models import CartItem, Product, Order, OrderProduct, Sale, User
from app import app, db
import jwt


@app.route('/orders', methods=['POST'])
def create_order():
    # Dekodowanie tokenu i uzyskiwanie user_id
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Unauthorized'}), 401

    try:
        # Usuwamy 'Bearer ' z tokenu
        token = token.split(' ')[1]
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = decoded_token['user_id']
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return jsonify({'message': 'Invalid token'}), 401

    # Pobranie danych z formularza
    data = request.json

    # Pobranie koszyka użytkownika
    cart = get_cart_for_user(user_id)
    if not cart:
        return jsonify({'message': 'Cart is empty'}), 400

    # Sprawdzenie dostępności produktów w koszyku
    for item in cart:
        product = get_product_by_id(item['id'])
        if product['quantity'] < item['quantity']:
            return jsonify({'message': f"Product {product['name']} is out of stock"}), 400

    # Obliczanie łącznej ceny zamówienia
    total_price = sum(item['quantity'] * item['price'] for item in cart)

    # Tworzenie zamówienia
    order = Order(
        user_id=user_id,
        first_name=data['first_name'],
        last_name=data['last_name'],
        address=data['address'],
        zip_code=data['zip_code'],
        city=data['city'],
        phone=data['phone'],
        total=total_price,
        status='PENDING'
    )

    # Dodanie zamówienia do bazy danych
    db.session.add(order)
    db.session.commit()

    # Zapisanie produktów w zamówieniu
    for item in cart:
        order_product = OrderProduct(order_id=order.id, product_id=item['id'], quantity=item['quantity'])
        db.session.add(order_product)

        # Aktualizacja stanu magazynowego (zmniejszenie dostępnej ilości produktów)
        product = Product.query.get(item['id'])
        if product:
            product.stock -= item['quantity']
            db.session.add(product)

            # Dodanie sprzedaży do tabeli Sales
            sale = Sale(
                order_product_id=order_product.id,
                product_id=product.id,
                quantity=item['quantity'],
                price_per_unit=product.price,
                total_price=item['quantity'] * product.price
            )
            db.session.add(sale)

    db.session.commit()

    # Usuwanie produktów z koszyka
    CartItem.query.filter_by(user_id=user_id).delete()
    db.session.commit()

    return jsonify({
        'message': 'Order created successfully',
        'order_id': order.id,
        'total': total_price
    }), 201


@app.route('/notify', methods=['POST'])
def notify():
    return '', 200


def get_cart_for_user(user_id):
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    cart = [
        {
            'id': item.product_id,
            'quantity': item.quantity,
            'price': float(item.product.price),
            'name': item.product.name
        }
        for item in cart_items
    ]
    return cart


def get_product_by_id(product_id):
    product = Product.query.get(product_id)
    if product:
        return {
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'quantity': product.stock
        }
    return None


@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    # Pobieranie zamówienia na podstawie ID
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404

    # Pobieranie produktów powiązanych z zamówieniem
    order_products = OrderProduct.query.filter_by(order_id=order.id).all()
    products = [
        {
            'product_id': op.product.id,
            'name': op.product.name,
            'price': float(op.product.price),
            'quantity': op.quantity
        }
        for op in order_products
    ]

    # Przygotowanie odpowiedzi JSON
    order_data = {
        'order_id': order.id,
        'first_name': order.first_name,
        'last_name': order.last_name,
        'address': order.address,
        'zip_code': order.zip_code,
        'city': order.city,
        'phone': order.phone,
        'total': float(order.total),
        'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'status': order.status,
        'products': products
    }

    return jsonify(order_data), 200


@app.route('/user/orders', methods=['GET'])
def get_user_orders():
    # Przykład identyfikacji użytkownika na podstawie tokenu
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Unauthorized'}), 401

    try:
        token = token.split(' ')[1]
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = decoded_token['user_id']
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return jsonify({'message': 'Invalid token'}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    orders = user.orders
    orders_data = [
        {
            'order_id': order.id,
            'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'total': float(order.total),
            'status': order.status
        }
        for order in orders
    ]

    return jsonify(orders_data), 200
