from flask_restful import Resource, abort
import json

shops_file = 'data/shops.json'
with open(shops_file) as f:
    Shops = json.load(f)


def abort_shop_doesnt_not_exist(shop_id):
    if shop_id not in Shops:
        abort(404, message="Shop {} doesn't exist".format(shop_id))


class Shop(Resource):
    def get(self, shop_id):
        abort_shop_doesnt_not_exist(shop_id)
        return Shops[shop_id]


class ShopList(Resource):
    def get(self):
        return Shops