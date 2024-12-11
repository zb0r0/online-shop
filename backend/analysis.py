from flask import request, jsonify
from models import Product, Sale, User, Order, OrderProduct
from app import app, db
from auth import admin_required


@app.route('/analysis/trends', methods=['GET'])
def sales_trends():
    month = request.args.get('month', type=int)
    if not month:
        return jsonify({'message': 'Missing "month" parameter'}), 400

    sales_data = (
        db.session.query(Product.name, db.func.sum(Sale.quantity).label('total_quantity'))
        .join(Sale, Sale.product_id == Product.id)
        .filter(db.extract('month', Sale.sold_at) == month)
        .group_by(Product.name)
        .order_by(db.desc('total_quantity'))  # Sortowanie po ilości sprzedanych produktów
        .all()
    )

    if not sales_data:
        return jsonify({'message': 'No sales data for the specified month'}), 404

    return jsonify([{
        'product_name': product_name,
        'total_quantity': int(total_quantity)
    } for product_name, total_quantity in sales_data]), 200


@app.route('/analysis/top-customers', methods=['GET'])
def top_customers():
    customer_data = (
        db.session.query(User.username, db.func.sum(Sale.total_price).label('total_spent'))
        .join(Order, Order.user_id == User.id)
        .join(OrderProduct, OrderProduct.order_id == Order.id)
        .join(Sale, Sale.order_product_id == OrderProduct.id)
        .group_by(User.username)
        .order_by(db.desc('total_spent'))
        .limit(10)
        .all()
    )

    if not customer_data:
        return jsonify({'message': 'No customer data found'}), 404

    return jsonify([{
        'username': username,
        'total_spent': float(total_spent)
    } for username, total_spent in customer_data]), 200



@app.route('/analysis/low-stock', methods=['GET'])
def low_stock():
    threshold = request.args.get('threshold', default=10, type=int)
    low_stock_products = Product.query.filter(Product.stock <= threshold).all()

    if not low_stock_products:
        return jsonify({'message': 'No low-stock products found'}), 404

    return jsonify([{
        'id': product.id,
        'name': product.name,
        'stock': product.stock
    } for product in low_stock_products]), 200

