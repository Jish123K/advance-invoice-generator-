from flask import Flask, request, jsonify

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import func

from typing import List

from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    product_name = db.Column(db.String(50), unique=True, nullable=False)

    quantity_left = db.Column(db.Float, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    deleted = db.Column(db.Boolean, default=False)

@app.route('/products', methods=['GET'])

def get_products():

    products = Product.query.filter(Product.deleted != True).all()

    return jsonify([{'id': p.id, 'product_name': p.product_name, 'quantity_left': p.quantity_left} for p in products])

@app.route('/products', methods=['POST'])

def create_product():

    product_name = request.json.get('product_name')

    quantity_left = request.json.get('quantity_left')

    if not product_name or not quantity_left:

        return jsonify({'error': 'product_name and quantity_left are required'}), 400

    product = Product(product_name=product_name, quantity_left=quantity_left)

    db.session.add(product)

    db.session.commit()

    return jsonify({'id': product.id, 'product_name': product.product_name, 'quantity_left': product.quantity_left}), 201

@app.route('/products/<int:id>', methods=['GET'])

def get_product(id):

    product = Product.query.filter(Product.id == id, Product.deleted != True).first()

    if not product:

        return jsonify({'error': f'product with id {id} was not found'}), 404

    return jsonify({'id': product.id, 'product_name': product.product_name, 'quantity_left': product.quantity_left})

@app.route('/products/<int:id>', methods=['PUT'])

def update_product(id):

    product = Product.query.filter(Product.id == id, Product.deleted != True).first()

    if not product:

        return jsonify({'error': f'product with id {id} was not found'}), 404

    product_name = request.json.get('product_name')

    quantity_left = request.json.get('quantity_left')

    if not product_name or not quantity_left:

        return jsonify({'error': 'product_name and quantity_left are required'}), 400

    product.product_name = product_name

    product.quantity_left = quantity_left

    db.session.commit()

    return jsonify({'id': product.id, 'product_name': product.product_name, 'quantity_left': product.quantity_left})

@app.route('/products/<int:id>', methods=['DELETE'])

def delete_product(id):

    product = Product.query.filter(Product.id == id, Product.deleted != True).first()

    if not product:

        return jsonify({'error': f'product with id {id} was not found'}), 404

    product.deleted = True

    db.session.commit()

    return '', 204

