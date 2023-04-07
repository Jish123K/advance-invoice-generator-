# app.py

from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/mydatabase'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(50), nullable=False)

    created_at = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.now(), nullable=False)

    deleted = db.Column(db.Boolean, nullable=False, server_default='false')

class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    product_name = db.Column(db.String(100), nullable=False)

    quantity_left = db.Column(db.Integer)

    quantity_init = db.Column(db.Integer)

    created_at = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.now(), nullable=False)

    deleted = db.Column(db.Boolean, nullable=False, server_default='false')

class Invoice(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    reference = db.Column(db.String(50), nullable=False)

    value_net = db.Column(db.BigInteger, nullable=False)

    actual_payment = db.Column(db.BigInteger, nullable=False)

    payment_due = db.Column(db.BigInteger, nullable=False)

    created_at = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.now(), nullable=False)

    deleted = db.Column(db.Boolean, nullable=False, server_default='false')

    invoice_owner_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

class InvoiceItem(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    product_name = db.Column(db.String(100), nullable=False)

    quantity = db.Column(db.Integer, nullable=False)

    prix_unit = db.Column(db.BigInteger, nullable=False)

    created_at = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.now(), nullable=False)

    deleted = db.Column(db.Boolean, nullable=False, server_default='false')

    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id', ondelete='CASCADE'), nullable=False)

# manage.py

from app import app, db, migrate

if __name__ == '__main__':

    app.run()

# command to create the initial migration

# flask db init

# command to create the migration script

# flask db migrate -m "create tables"

# command to apply the migration

# flask db upgrade

