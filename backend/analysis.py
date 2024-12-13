from flask import request, jsonify
from models import Product, Sale, User, Order, OrderProduct
from app import app, db
from auth import admin_required
from datetime import datetime
from sqlalchemy.sql import extract


@app.route('/analysis/trends', methods=['GET'])
def sales_trends():
    start_date = request.args.get('start_date', type=str)
    end_date = request.args.get('end_date', type=str)

    if not start_date or not end_date:
        return jsonify({'message': 'Both "start_date" and "end_date" parameters are required'}), 400

    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return jsonify({'message': 'Invalid date format. Please use "YYYY-MM-DD".'}), 400

    sales_data = (
        db.session.query(Product.name, db.func.sum(Sale.quantity).label('total_quantity'))
        .join(Sale, Sale.product_id == Product.id)
        .filter(Sale.sold_at >= start_date, Sale.sold_at <= end_date)
        .group_by(Product.name)
        .order_by(db.desc('total_quantity'))
        .all()
    )

    if not sales_data:
        return jsonify({'message': 'No sales data for the specified date range'}), 404

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


@app.route('/analysis/earnings', methods=['GET'])
def earnings_analysis():
    # Pobranie parametrów z zapytania
    view_type = request.args.get('view_type', type=str)
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)

    if not view_type or view_type not in ['year', 'month', 'day']:
        return jsonify({'message': 'Invalid or missing "view_type" parameter. Allowed values: year, month, day'}), 400

    try:
        query = db.session.query(
            db.func.sum(Order.total).label('total_earnings')
        )

        if view_type == 'year':
            # Widok roczny: grupowanie danych według lat
            query = query.add_columns(db.func.extract('year', Order.created_at).label('year'))
            query = query.group_by('year')

        elif view_type == 'month':
            if not year:
                return jsonify({'message': 'Parameter "year" is required for view_type "month"'}), 400
            # Widok miesięczny: grupowanie danych według miesięcy w wybranym roku
            query = query.add_columns(db.func.extract('month', Order.created_at).label('month'))
            query = query.filter(db.func.extract('year', Order.created_at) == year)
            query = query.group_by('month')

        elif view_type == 'day':
            if not year or not month:
                return jsonify({'message': 'Parameters "year" and "month" are required for view_type "day"'}), 400
            # Widok dzienny: grupowanie danych według dni w wybranym miesiącu i roku
            query = query.add_columns(db.func.extract('day', Order.created_at).label('day'))
            query = query.filter(db.func.extract('year', Order.created_at) == year,
                                 db.func.extract('month', Order.created_at) == month)
            query = query.group_by('day')

        results = query.all()

        if not results:
            return jsonify({'message': 'No earnings data found for the specified parameters'}), 404

        response = []
        for result in results:
            if view_type == 'year':
                response.append({
                    'year': int(result.year),
                    'total_earnings': float(result.total_earnings)
                })
            elif view_type == 'month':
                response.append({
                    'month': int(result.month),
                    'total_earnings': float(result.total_earnings)
                })
            elif view_type == 'day':
                response.append({
                    'day': int(result.day),
                    'total_earnings': float(result.total_earnings)
                })

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'message': 'An error occurred while processing the request', 'error': str(e)}), 500
