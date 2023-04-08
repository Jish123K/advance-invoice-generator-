from flask import Flask, jsonify

from flask_cors import CORS

from . import models

from .database import engine

from .routers import user, auth, invoice, product

from .config import settings

# models.Base.metadata.create_all(bind=engine)

app = Flask(__name__)

CORS(app)

app.register_blueprint(auth.router)

app.register_blueprint(user.router)

app.register_blueprint(product.router)

app.register_blueprint(invoice.router)

@app.route("/")

def root():

    return jsonify({"message": "Hello World pushing out", "hi": "Hello"})

if __name__ == '__main__':

    app.run()
