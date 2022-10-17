from flask import request
from db import db
from flask_restful import Resource
from flask_login import current_user
from flask_security import roles_required


from models.product_model import Product
class Products(Resource):
    @roles_required('admin')
    def post(self):
        data = request.get_json()
        if data:
            if not Product.find_in_db(data['name']):
                product = Product(data['name'], data['label'], data['price'], data['description'], current_user.id)
                try:
                    product.add_to_products()
                    return True
                except:
                    return {'message': 'an error has occured...!'}
            return False

    @roles_required('admin')
    def delete(self, id):
        product = Product.query.filter_by(id=id).first()
        print(product)
        if product:
            product.delete_from_products()
            return True
        return {"message": "couldn't find this product id"}

    @roles_required('admin')
    def put(self):
        data = request.get_json()
        product = Product.query.filter_by(id=data['id']).first()

        for key, value in data.items():
            if hasattr(product, key):
                try:
                    setattr(product, key, value)
                    db.session.commit()
                except:
                    return False
        return True



class GetAllProducts(Resource):
    @roles_required('admin')
    def get(self):
        return {'Products': list(map(lambda x: x.products_fetch(), Product.query.all()))}


class ProductsFilter(Resource):
    def get(self, label):
        data = Product.query.filter_by(label=label).all()
        return list(map(lambda x: x.products_fetch(), data))
