from db import db
from flask import request

from models.product_model import Product

class Order_items(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User')

    product_id = db.Column(db.Integer)
    quantity = db.Column(db.String(80))

    def __init__ (self, product_id, quantity, user_id):
        self.quantity = quantity
        self.product_id = product_id
        self.user_id = user_id

    def info(self):
        product = Product.query.filter_by(id=self.product_id).first()
        return {
            'id': self.id,
            'user_id': self.user.id,
            'user_first_name': self.user.first_name,
            'product name': product.name,
            'price': product.price
        }


    def add_to_orders(self):
        db.session.add(self)
        db.session.commit()


    def delete_from_orders(self):
        db.session.delete(self)
        db.session.commit()
