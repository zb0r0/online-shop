from flask import request, jsonify
from models import Product
from app import app, db
from auth import admin_required


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
