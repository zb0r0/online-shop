from flask import request, jsonify
import requests
from models import CartItem, Product, Order, User
from app import app, db
import jwt
import logging

PAYU_POS_ID = '300746'
PAYU_CLIENT_SECRET = '2ee86a66e5d97e3fadc400c9f19b065d'
PAYU_API_URL = 'https://secure.snd.payu.com/api/v2_1/orders'
PAYU_AUTH_URL = 'https://secure.snd.payu.com/pl/standard/user/oauth/authorize'

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
        product = get_product_by_id(item['product_id'])
        if product['quantity'] < item['quantity']:
            return jsonify({'message': f"Product {product['name']} is out of stock"}), 400

    # Obliczanie łącznej ceny zamówienia
    total_price = sum(item['quantity'] * item['price'] for item in cart)

    # Przygotowanie danych do płatności
    order_data = {
        "notifyUrl": "https://48.209.24.37:5000/notify",
        "customerIp": request.remote_addr,
        "merchantPosId": PAYU_POS_ID,
        "description": "Sklep internetowy - zamówienie",
        "currencyCode": "PLN",
        "totalAmount": str(int(total_price * 100)),
        "buyer": {
            "email": data['email'],
            "phone": data['phone'],
            "firstName": data['first_name'],
            "lastName": data['last_name'],
            "language": "pl"
        },
        "products": [
            {
                "name": item['name'],
                "unitPrice": str(int(item['price'] * 100)),
                "quantity": item['quantity']
            } for item in cart
        ],
        "continueUrl": "https://48.209.24.37:8080/notify"
    }

    # Pobranie tokenu dostępu PayU
    access_token = get_payu_access_token()
    if not access_token:
        return jsonify({'message': 'Failed to obtain access token from PayU'}), 500

    # Wysłanie żądania do PayU
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(PAYU_API_URL, json=order_data, headers=headers, allow_redirects=False)
    except Exception as e:
        return jsonify({'message': f'Error during PayU API call: {str(e)}'}), 500

    # Logowanie odpowiedzi
    print("Response status code:", response.status_code)
    print("Raw response text:", response.text)

    if response.status_code in (200, 201):
        return jsonify({
            'payment_url': response.json().get('redirectUri'),
            'total': total_price
        }), 200
    elif response.status_code == 302:
        return jsonify({'payment_url': response.headers.get('Location')}), 200
    else:
        # Obsługa błędów
        return jsonify({
            'message': 'Error from PayU',
            'details': response.text,
            'status_code': response.status_code
        }), 500


def get_payu_access_token():
    try:
        response = requests.post(
            PAYU_AUTH_URL,
            data={
                'grant_type': 'client_credentials',
                'client_id': PAYU_POS_ID,
                'client_secret': PAYU_CLIENT_SECRET
            }
        )
        print("PayU Auth Response:", response.text)

        if response.status_code == 200:
            return response.json().get('access_token')
        else:
            logging.error(f"Failed to obtain PayU access token: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logging.error(f"Error during PayU access token request: {str(e)}")
        return None


@app.route('/notify', methods=['POST'])
def notify():
    # Obsługa notyfikacji PayU po udanej płatności
    payload = request.json
    print(payload)
    if payload['order']['status'] == 'COMPLETED':
        update_order_status(payload['order']['orderId'], 'COMPLETED')
        reduce_product_quantities(payload['order']['products'])
        reset_cart(payload['order']['buyer']['email'])
        return '', 200
    return '', 400


def get_cart_for_user(user_id):
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    cart = [
        {
            'product_id': item.product_id,
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


def update_order_status(order_id, status):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404

    # Zaktualizuj status zamówienia
    order.status = status
    db.session.commit()

    return jsonify({'message': 'Order status updated successfully'}), 200


def reduce_product_quantities(products):
    for product in products:
        product_id = product['id']
        quantity = product['quantity']
        product = Product.query.get(product_id)
        if product and product.stock >= quantity:
            product.stock -= quantity
    db.session.commit()


def reset_cart(email):
    user = User.query.filter_by(email=email).first()
    if user:
        CartItem.query.filter_by(user_id=user.id).delete()
        db.session.commit()
