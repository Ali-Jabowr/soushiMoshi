from db import db
from flask import request, session


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique = True)
    label = db.Column(db.String(80))
    price = db.Column(db.Integer)
    description = db.Column(db.String(255))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    user = db.relationship('User', back_populates="products")

    def __init__(self, name, label, price, description, user_id):
        self.name = name
        self.label = label
        self.price = price
        self.description = description
        self.user_id = user_id

    def products_fetch(self):
        return {
            'id': self.id,
            'name': self.name,
            'label':self.label,
            'price': self.price,
            'description': self.description,
        }

    def display(self):
        return {
            'name': self.name,
            'label': self.label,
            'price': self.price,
            'description': self.description
        }

    @classmethod
    def find_in_db(cls, name):
        return cls.query.filter_by(name=name).first()

    def fetch_the_session():
        products = []
        for item in session['order']:
            product = Product.query.filter_by(id=item['id']).first()
            quantity = item['quantity']

            products.append({'id': product.id,
                             'name': product.name,
                             'price': product.price,
                             'quantity': quantity
                             })
        return products




    def add_to_products(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_products(self):
        db.session.delete(self)
        db.session.commit()
