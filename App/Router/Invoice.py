from flask import Blueprint, jsonify, request

from sqlalchemy import func

from app import db

from app.models import Invoice, InvoiceItem

from app.auth import auth_required

invoices_bp = Blueprint('invoices', __name__, url_prefix='/invoices')

@invoices_bp.route('/', methods=['GET'])

@auth_required

def get_invoices():

    invoices = Invoice.query.all()

    return jsonify([invoice.to_dict() for invoice in invoices])

@invoices_bp.route('/', methods=['POST'])

@auth_required

def create_invoice():

    data = request.get_json()

    post_data = data.get('post')

    item_data = data.get('item')

    invoice = Invoice(post_data)

    db.session.add(invoice)

    for item in item_data:

        invoice_item = InvoiceItem(item, invoice.id)

        db.session.add(invoice_item)

    db.session.commit()

    return jsonify(invoice.to_dict())

@invoices_bp.route('/<int:id>', methods=['GET'])

@auth_required

def get_invoice(id):

    invoice = Invoice.query.get_or_404(id)

    return jsonify(invoice.to_dict())

@invoices_bp.route('/<int:id>', methods=['PUT'])

@auth_required

def update_invoice(id):

    invoice = Invoice.query.get_or_404(id)

    data = request.get_json()

    post_data = data.get('post')

    item_data = data.get('item')

    invoice.update(post_data)

    InvoiceItem.query.filter_by(invoice_id=invoice.id).delete()

    for item in item_data:

        invoice_item = InvoiceItem(item, invoice.id)

        db.session.add(invoice_item)

    db.session.commit()

    return jsonify(invoice.to_dict())

@invoices_bp.route('/<int:id>', methods=['DELETE'])

@auth_required

def delete_invoice(id):

    invoice = Invoice.query.get_or_404(id)

    db.session.delete(invoice)

    db.session.commit()

    return '', 204

