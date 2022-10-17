import re
from db import db
from flask import request, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from flask_restful import Resource
import wtforms_json
from werkzeug.security import check_password_hash, generate_password_hash
from flask_security import roles_required,SQLAlchemyUserDatastore

from models.users_model import User, RegisterForm, LoginForm, Role
from models.product_model import Product
from models.orders_model import Order_items

wtforms_json.init()
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

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
                user_role = user_datastore.find_or_create_role('user')
                user_datastore.add_role_to_user(user, user_role)
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
        user = User.query.filter_by(id=current_user.id).first()
        return {'user': user.profile()}

    def put(self):
        data = request.get_json()

        user = User.query.filter_by(email=data['email']).first()
        if user != None and current_user.email != data['email']:
            return {'message': 'Email already registered'}
        user = User.query.filter_by(phone_number=data['phone_number']).first()
        if user != None and current_user.phone_number != data['phone_number']:
            return {'message': 'this phone number already used'}

        user = User.query.filter_by(id=current_user.id).first()
        for key, value in data.items():
            if hasattr(user, key):
                try:
                    setattr(user, key, value)
                    db.session.commit()
                except:
                    return False
        return True

class Admin_area(Resource):
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
                user_role = user_datastore.find_or_create_role('admin')
                user_datastore.add_role_to_user(user, user_role)
                user.add_to_db()
                return True
            except:
                return False

        return {'message': [(key, err) for key, err in form.errors.items()]}

    @roles_required('admin')
    def get(self):
        return {'message': 'you are not allowed ... '}
