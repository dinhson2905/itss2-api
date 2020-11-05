from flask import Flask
from flask_restful import Resource, Api
from resource import products, shops


app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'World'}

api.add_resource(HelloWorld, '/')
api.add_resource(products.ProductList, '/products')
api.add_resource(products.Product, '/products/<product_id>')
api.add_resource(shops.ShopList, '/shops')
api.add_resource(shops.Shop, '/shops/<shop_id>')

if __name__ == "__main__":
    app.run(debug=True)