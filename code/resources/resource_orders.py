from db import db
from flask_restful import Resource
from flask import request

from models.orders_model import Order

class Orders(Resource):
    def get(self):
        return {'info': list(map(lambda x: x.get_info(), Order.query.all()))}

