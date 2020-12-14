from bson import json_util
from flask import Flask, request, jsonify, make_response, json
from flask_restful import Resource, Api
from resource import products, shops
from flask_cors import CORS, cross_origin
from flask_mail import Mail, Message
import db

app = Flask(__name__)
CORS(app, support_credentials=True)
api = Api(app)
mail = Mail(app)  # instantiate the mail class

# configuration of mail
app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '7f30d76d1b1876'
app.config['MAIL_PASSWORD'] = '41062c9954ad8c'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)


# test to insert data to the data base
@app.route("/test")
def test():
    db.db.collection.insert_one({"name": "John"})
    return "Connected to the data base!"


def parse_json(data):
    return json.loads(json_util.dumps(data))


@app.route("/comment/saveComment", methods=['POST'])
@cross_origin(supports_credentials=True)
def createComment():
    # print(request.json, flush=True)
    data = request.json
    name = data['name']
    content = data['content']
    postId = data['postId']

    comment = {
        "name": name,
        "content": content,
        "postId": postId
    }
    _id = db.db.collection.insert_one(comment)
    print(_id.inserted_id)
    result = parse_json(db.db.collection.find({"_id": _id.inserted_id}))
    response = jsonify(status=200, data=result)
    print(response)
    # return make_response(jsonify(result), "success")
    return response


@app.route("/comment/getComment", methods=['POST'])
@cross_origin(supports_credentials=True)
def getComment():
    # print(request.json, flush=True)
    data = request.json
    postId = data['id']
    #
    result = parse_json(db.db.collection.find({"postId": postId}))
    response = jsonify(status=200, data=result)
    print(response)
    # # return make_response(jsonify(result), "success")
    return response


@app.route("/ ")
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'World'}


api.add_resource(HelloWorld, '/')
api.add_resource(products.ProductList, '/products')
api.add_resource(products.Product, '/products/<product_id>')
api.add_resource(shops.ShopList, '/shops')
api.add_resource(shops.Shop, '/shops/<shop_id>')


@app.route('/send', methods=['POST'])
def send():
    content = request.json
    print(content['email'])
    msg = Message("Feedback", sender=content['email'], recipients=['thanhcong.phung@gmail.com'])
    msg.body = content['message']
    mail.send(msg)
    return jsonify(status='success')


if __name__ == "__main__":
    app.run(debug=True)
