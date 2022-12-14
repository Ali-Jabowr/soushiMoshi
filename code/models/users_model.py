from db import db
from flask import request
from flask_login import UserMixin, current_user
from flask_rbac import RBAC
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import InputRequired, Email, DataRequired, EqualTo, Length
from flask_security import RoleMixin

from models.product_model import Product
from models.orders_model import Order_items



# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    father_name = db.Column(db.String(80))
    street = db.Column(db.String(80))
    appartment = db.Column(db.String(80))
    building = db.Column(db.String(80))
    phone_number = db.Column(db.String(12), unique=True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))

    products = db.relationship('Product', back_populates="user")
    orders = db.relationship('Order_items', back_populates='user')
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


    def __init__(self,
                 last_name, first_name, father_name,
                 email, password, phone_number,
                 street, building, appartment):

        self.last_name = last_name
        self.first_name = first_name
        self.father_name = father_name
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.street = street
        self.building = building
        self.appartment = appartment

    @classmethod
    def find_in_db(cls, email):
        return cls.query.filter_by(email=email).first()


    @classmethod
    def check_in_db(cls, email, password):
        res = cls.query.filter_by(email=email).first()
        if res:
            if check_password_hash(res.password, password):
                return res

    def update_info(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
                db.session.commit()


    def json(self):
        orders = Order_items.query.filter_by(user_id=self.id)
        return{
            'id': self.id,
            'last_name': self.last_name,
            'first_name': self.first_name,
            'father_name': self.father_name,
            'email': self.email,
            'password': self.password,
            'phone_number': self.phone_number,
            'address': {
                'street': self.street,
                'building': self.building,
                'appartment': self.appartment
            },
            'orders_quantity': len(orders.all()),
            'orders': list(map(lambda x: x.info(), orders))
        }

    def profile(self):
        orders = Order_items.query.filter_by(user_id=self.id)
        return{
            'last_name': self.last_name,
            'first_name': self.first_name,
            'father_name': self.father_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'address': {
                'street': self.street,
                'building': self.building,
                'appartment': self.appartment
            },
            'orders_quantity': len(orders.all()),
            'orders': list(map(lambda x: x.user_view(), orders))
        }

    def user_info(self):
        orders = Order_items.query.filter_by(user_id=self.id)
        return{
            'last_name': self.last_name,
            'first_name': self.first_name,
            'father_name': self.father_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'address': {
                'street': self.street,
                'building': self.building,
                'appartment': self.appartment
            }
        }

    def add_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class RegisterForm(Form):
    last_name = StringField('last_name', validators=[DataRequired(), Length(min=3, max=32)])
    first_name = StringField('first_name', validators=[DataRequired(),  Length(min=3, max=32)])
    father_name = StringField('father_name', validators=[DataRequired(),  Length(min=3, max=32)])
    street = StringField('street',validators=[DataRequired()])
    appartment = StringField('appartment', validators=[DataRequired()])
    building = IntegerField('building', validators=[DataRequired()])
    phone_number = StringField('phone_number', validators=[DataRequired(), Length(min=12, max=12)])
    email = StringField('email', validators=[DataRequired(),Email(check_deliverability=True),  Length(min=6, max=40)])
    password = StringField('password', validators=[DataRequired(), Length(min=8, max=64)])
    repeatPassword = StringField('repeatPassword', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(first_name=self.first_name.data).first()
        if user:
            self.first_name.errors.append("Username already registered")
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        user = User.query.filter_by(phone_number=self.phone_number.data).first()
        if user:
            self.phone_number.errors.append("Phone number already registered")
            return False
        return True


class LoginForm(Form):
    email = StringField('Email',
            validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if not user:
            self.email.errors.append('Unknown email')
            return False
        if not check_password_hash(user.password, self.password.data):
            self.password.errors.append('Invalid password')
            return False
        return True
