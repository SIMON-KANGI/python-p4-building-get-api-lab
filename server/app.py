#!/usr/bin/env python3

from flask import Flask, make_response, jsonify,request
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries',methods=['GET', 'POST'])  
def bakeries():
    if request.method == 'GET':
        backeries=[ backeries.to_dict() for backeries in Bakery.query.all()]
        response=make_response(
            jsonify(backeries),
            200,
            {'content-type': 'application/json'}
        )
        return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery=Bakery.query.filter_by(id=id).first()
    if bakery:
        return jsonify(bakery.to_dict())
    else:
        return jsonify({'message': 'Bakery not found.'}, 404)


@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods=BakedGood.query.order_by(BakedGood.price).all()
    baked_goods_dict=[baked_goods.to_dict() for baked_goods in baked_goods]
    return jsonify(baked_goods_dict)
    

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    expensive_goods=BakedGood.query.order_by(BakedGood.price.desc()).first()
    
    if expensive_goods:
        return jsonify(expensive_goods.to_dict())
    else:
        return jsonify({'message': 'No baked goods found.'})

if __name__ == '__main__':
    app.run(port=5555, debug=True)
