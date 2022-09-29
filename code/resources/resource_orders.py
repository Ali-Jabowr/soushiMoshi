from db import db
from flask import request, session
from flask_restful import Resource
from flask_login import current_user

from models.product_model import Product
from models.orders_model import Order_items

class Orders(Resource):
    def get(self):
        return {'info': list(map(lambda x: x.get_info(), Order.query.all()))}


class AddToSession(Resource):
    def post(self):
        if 'order' not in session:
            session['order'] = []
        else:
            session['order'] = []

        data = request.get_json()
        if data:
            session['order'].append({'id': data['id'], 'quantity': data['quantity']})
            session.modified = True
        return {'session': session['order']}


class AddOrder(Resource):
    def post(self):
        products = Product.fetch_the_session()

        for product in products:
            order = Order_items(product['id'], product['quantity'], current_user.id)
            if order:
                try:
                    order.add_to_orders()
                    return True
                except:
                    return False
            return {'message': 'an error has occured...'}

    def get(self):
        orders = Order_items.query.all()
        if orders:
            return {'orders': list(map(lambda x: x.info(), orders))}
        return {'message': 'an error has occured...'}

    def delete(self, id):
        order = Order_items.query.filter_by(id=id).first()
        try:
            order.delete_from_orders()
            return True
        except:
            return False


