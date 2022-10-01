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
        products = request.get_json()

        for product in products['orders']:

            product_id = Product.query.filter_by(id=product['id']).first()
            if not product_id:
                return {'message': 'there are no such product...',
                        'product_id': product['id']
                        }

            order = Order_items(
                product['id'],
                product['quantity'],
                current_user.id)
            if order:
                try:
                    order.add_to_orders()
                except:
                    return False
        return True


    def get(self):
        orders = Order_items.query.all()
        if orders:
            return {'orders': list(map(lambda x: x.info(), orders))}
        return {'message': 'an error has occured...'}

    def delete(self):
        data = request.get_json()
        orders = Order_items.query.all()
        if data['delete'] == "all":
            orders = Order_items.query.filter_by(user_id=current_user.id).all()
            for order in orders:
                try:
                    order.delete_from_orders()
                except:
                    return {'message': 'an error has occured...'}
            return True

        else:
            for id in data['delete']:
                order = Order_items.query.filter_by(id=id).first()
                if order != None and current_user.id != order.user_id:
                    return{'message': 'you are not allowed to do this...'}
                try:
                    order.delete_from_orders()
                except:
                    return False, 404
            return True


