from db import db
from flask import request


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'))
    product = db.relationship('Product')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates="order")


    def get_info(self):
        print("here")
        return {
            'user_id': self.user.id,
            'product_id': self.product.id
        }
