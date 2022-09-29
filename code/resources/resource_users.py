import re
from flask import request, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from flask_restful import Resource
import wtforms_json
from werkzeug.security import check_password_hash, generate_password_hash

from models.users_model import User, RegisterForm, LoginForm
from models.product_model import Product

wtforms_json.init()

class UserReg(Resource):
    def post (self):
        data = request.get_json()
        form = RegisterForm.from_json(data, skip_unknown_keys=False)
        if form.validate():
            password_hash = generate_password_hash(form.password.data)
            user = User(
                form.last_name.data,
                form.first_name.data,
                form.father_name.data,
                form.email.data,
                password_hash,
                form.phone_number.data,
                form.street.data,
                form.building.data,
                form.appartment.data
            )

            try:
                user.add_to_db()
                return True
            except:
                return False

        return {'message': [(key, err) for key, err in form.errors.items()]}



class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        form = LoginForm.from_json(data, skip_unknown_keys=False)
        if form.validate():
            user = User.query.filter_by(email=data['email']).first()
            login_user(user)
            return True

        return {'message': [err for _, err in form.errors.items()]}

class UserLogout(Resource):
    @login_required
    def post(self):
        logout_user()
        return {'message': 'User Logged Out'}


class GetUsers(Resource):
    def get(self):
        return list(map(lambda x: x.json(), User.query.all()))

class Profile(Resource):
    @login_required
    def get(self):
        return {'orders': Product.fetch_the_session()}

