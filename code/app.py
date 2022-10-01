from db import db
from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_login import LoginManager
from os import path

from resources.resource_users import UserReg, UserLogin, GetUsers, UserLogout, Profile
from resources.resource_products import Products, GetAllProducts, ProductsFilter
from resources.resource_orders import Orders, AddToSession, AddOrder
from models.users_model import User

app = Flask(__name__)
api = Api(app)
migrate = Migrate(app, db)


DB_NAME = 'data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SQLALCHEMY_TRACK_NOTIFICATION'] = False
app.config['SECRET_KEY'] = "mySecret"

app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_SECRET_KEY'] = 'myanothersecret'
app.config['WTF_CSRF_TIM_LIMIT'] = 3600


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# user endpoints
api.add_resource(UserReg, '/user/register')
api.add_resource(UserLogin, '/user/login')
api.add_resource(GetUsers, '/users')
api.add_resource(UserLogout, '/user/logout')
api.add_resource(Profile, '/user/profile', '/user/profile/edit')

# orders endpoints
api.add_resource(AddOrder, '/orders/order', '/orders/getorders', '/orders/delete')

# products endpoints
api.add_resource(Products, '/products/add',
                           '/products/delete/<int:id>',
                           '/products/edit')
api.add_resource(GetAllProducts, '/products/getproducts')
api.add_resource(ProductsFilter, '/products/<string:label>')


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("DATABASE CREATED SUCCESSFULY")
    app.run(debug=True)
