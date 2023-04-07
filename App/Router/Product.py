from flask import Blueprint, jsonify, request

from app import db

from app.models import Product

from app.auth import auth_required

products_bp = Blueprint('products', __name__, url_prefix='/products')

@products_bp.route('/', methods=['GET'])

@auth_required

def get_products():

    products = Product.query.all()

    return jsonify([product.to_dict() for product in products])

@products_bp.route('/', methods=['POST'])

@auth_required

def create_product():

    data = request.get_json()

    post_data = data.get('post')

    product = Product(post_data)

    db.session.add(product)

    db.session.commit()

    return jsonify(product.to_dict())

@products_bp.route('/<int:id>', methods=['GET'])

@auth_required

def get_product(id):

    product = Product.query.get_or_404(id)

    return jsonify(product.to_dict())

@products_bp.route('/<int:id>', methods=['PUT'])

@auth_required

def update_product(id):

    product = Product.query.get_or_404(id)

    data = request.get_json()

    post_data = data.get('post')

    product.update(post_data)

    db.session.commit()

    return jsonify(product.to_dict())

@products_bp.route('/<int:id>', methods=['DELETE'])

@auth_required

def delete_product(id):

    product = Product.query.get_or_404(id)

    db.session.delete(product)

    db.session.commit()

    return '', 204

