from flask import Flask
from flask_restful import Api, reqparse, abort, Resource
import json


products_file = 'data/products.json'
with open(products_file) as f:
    Products = json.load(f)


def abort_if_product_doesnt_exist(product_id):
    if product_id not in Products:
        abort(404, message="Product {} doesn't exist".format(product_id))

class ProductList(Resource):
    def get(self):
        return Products

class Product(Resource):
    def get(self, product_id):
        abort_if_product_doesnt_exist(product_id)
        return Products[product_id]
