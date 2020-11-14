from flask import Flask,request,jsonify
from flask_restful import Resource, Api
from resource import products, shops
from flask_cors import CORS
from flask_mail import Mail, Message

app = Flask(__name__)
CORS(app)
api = Api(app)
mail = Mail(app) # instantiate the mail class 


# configuration of mail 
app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '7f30d76d1b1876'
app.config['MAIL_PASSWORD'] = '41062c9954ad8c'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app) 

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'World'}

api.add_resource(HelloWorld, '/')
api.add_resource(products.ProductList, '/products')
api.add_resource(products.Product, '/products/<product_id>')
api.add_resource(shops.ShopList, '/shops')
api.add_resource(shops.Shop, '/shops/<shop_id>')

@app.route('/send',methods=['POST'])
def send():
    content = request.json
    print(content['email'])
    msg = Message("Feedback", sender=content['email'],recipients = ['thanhcong.phung@gmail.com']) 
    msg.body = content['message']
    mail.send(msg) 
    return jsonify(content)
if __name__ == "__main__":
    app.run(debug=True)