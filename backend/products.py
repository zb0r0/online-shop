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


@app.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404

    product_details = {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': float(product.price),
        'category': product.category,
        'stock': product.stock,
        'image_url': product.image_url,
        'tags': product.tags,
        'gender': product.gender,
        'status': product.status
    }
    return jsonify(product_details), 200


@app.route('/category/<string:category>', methods=['GET'])
def get_products_by_category(category):
    products = Product.query.filter(Product.category.ilike(category)).all()
    if not products:
        return jsonify({'message': 'No products found in this category'}), 404

    products_list = [
        {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': float(product.price),
            'stock': product.stock,
            'image_url': product.image_url
        }
        for product in products
    ]
    return jsonify(products_list), 200


@app.route('/products_by_category', methods=['GET'])
def get_normalized_categories():
    # Pobierz wszystkie unikalne kategorie z bazy danych
    categories = db.session.query(Product.category).distinct().all()

    # Jeśli nie ma kategorii, zwróć pustą listę
    if not categories:
        return jsonify([]), 200

    # Wyciągnij kategorie, normalizuj i usuń duplikaty
    normalized_categories = {category[0].strip().capitalize() for category in categories if category[0]}

    # Zamień zbiór na posortowaną listę
    normalized_categories = sorted(normalized_categories)

    return jsonify(normalized_categories), 200

