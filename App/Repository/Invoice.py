from flask import Flask, request

from flask_restful import Api, Resource, reqparse, fields, marshal_with

from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker, relationship

from typing import List

app = Flask(__name__)

api = Api(app)

engine = create_engine('sqlite:///invoices.db')

Session = sessionmaker(bind=engine)

Base = declarative_base()

class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True, index=True)

    password = Column(String)

class Product(Base):

    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)

    product_name = Column(String, unique=True, index=True)

    quantity_left = Column(Float)

class Invoice(Base):

    __tablename__ = 'invoices'

    id = Column(Integer, primary_key=True, index=True)

    invoice_owner_id = Column(Integer, ForeignKey('users.id'))

    payment_due = Column(Float)

    value_net = Column(Float)

    actual_payment = Column(Float)

    deleted = Column(Boolean, default=False)

    owner = relationship('User', backref='invoices')

    items = relationship('InvoiceItem', backref='invoice')

class InvoiceItem(Base):

    __tablename__ = 'invoice_items'

    id = Column(Integer, primary_key=True, index=True)

    invoice_id = Column(Integer, ForeignKey('invoices.id'))

    product_id = Column(Integer, ForeignKey('products.id'))

    quantity = Column(Float)

    product = relationship('Product', backref='invoice_items')

Base.metadata.create_all(bind=engine)

class UserResource(Resource):

    def post(self):

        parser = reqparse.RequestParser()

        parser.add_argument('username', type=str, required=True)

        parser.add_argument('password', type=str, required=True)

        args = parser.parse_args()

        session = Session()

        user = User(username=args['username'], password=args['password'])

        session.add(user)

        session.commit()

        return {'id': user.id, 'username': user.username}

class ProductResource(Resource):

    def post(self):

        parser = reqparse.RequestParser()

        parser.add_argument('product_name', type=str, required=True)

        parser.add_argument('quantity_left', type=float, required=True)

        args = parser.parse_args()

        session = Session()

        product = Product(product_name=args['product_name'], quantity_left=args['quantity_left'])

        session.add(product)

        session.commit()

        return {'id': product.id, 'product_name': product.product_name, 'quantity_left': product.quantity_left}

class InvoiceResource(Resource):

    invoice_fields = {

        'id': fields.Integer,

        'invoice_owner_id': fields.Integer,

        'payment_due': fields.Float,

        'value_net': fields.Float,

        'actual_payment': fields.Float,

        'deleted': fields.Boolean,

        'items': fields.List(fields.Nested({

            'id': fields.Integer,

            'product_name': fields.String,

            'quantity': fields.Float,

        }))

    }

    @marshal_with(invoice_fields)

    def get(self, id):

        session = Session()

        invoice = session.query(Invoice).filter(Invoice.id == id, Invoice.deleted != True).first()

        if not invoice:

            api.abort(404, message=f"Invoice with id {id} was not found")

        return invoice

    @marshal_with(invoice_fields)

    def post(self):

        parser = req
uestParser()
    session = Session()

    invoice = Invoice(invoice_owner_id=args['invoice_owner_id'],

                      payment_due=args['payment_due'],

                      value_net=args['value_net'],

                      actual_payment=args['actual_payment'])
                      api.add_resource(UserResource, '/users')

api.add_resource(ProductResource, '/products')

api.add_resource(InvoiceResource, '/invoices', '/invoices/int:id')

if name == 'main':

app.run(debug=True)

    session.add(invoice)

    session.commit()

    return invoice


parser.add_argument('invoice_owner_id', type=int, required=True)

parser.add_argument('payment_due', type=float, required=True)

parser.add_argument('value_net', type=float, required=True)

parser.add_argument('actual_payment', type=float, required=True)

args = parser.parse_args()
