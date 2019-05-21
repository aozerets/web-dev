#! /usr/bin/env python3

from flask import Flask, jsonify, render_template
import random
from string import ascii_lowercase

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
PRODUCTS = [
    {
        "name": "Laptop" + str(x),
        "cost": str(x*100) + "z",
        "id": x,
        "brand": "BRAND  " + str(x),
        "comment": "".join([(str(ascii_lowercase[random.randint(0, 25)]*y*5) + " ") for y in range(10)])
    } for x in range(10)
]


@app.route('/')
@app.route('/<name>/')
def index_page(name=None):
    response = render_template(
        'index.html',
        name=name
    )
    return response


@app.route('/products/')
def products_page():
    response = render_template(
        'products.html',
        products=PRODUCTS
    )
    return response


@app.route('/products/<int:prod_id>/')
def product_page(prod_id):
    response = render_template(
        'product.html',
        product=next((x for x in PRODUCTS if x['id'] == prod_id), None)
    )
    return response


if __name__ == '__main__':
    app.run()
