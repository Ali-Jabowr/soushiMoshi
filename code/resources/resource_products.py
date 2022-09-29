from flask import request
from flask_restful import Resource
from flask_login import current_user


from models.product_model import Product
class Products(Resource):
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

    def delete(self, id):
        product = Product.query.filter_by(id=id).first()
        print(product)
        if product:
            product.delete_from_products()
            return True
        return {"message": "couldn't find this product id"}



class GetAllProducts(Resource):
    def get(self):
        return {'Products': list(map(lambda x: x.products_fetch(), Product.query.all()))}


class ProductsFilter(Resource):
    def get(self, label):
        data = Product.query.filter_by(label=label).all()
        return list(map(lambda x: x.products_fetch(), data))
