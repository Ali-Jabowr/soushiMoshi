from db import db
from flask request import request
from flask_login import UserMixin
from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import InputRequired, Email, DataRequired, EqualTo, Length


class AdminRegisterForm(Form):
    last_name = StringField('last_name', validators=[DataRequired(), Length(min=3, max=32)])
    first_name = StringField('first_name', validators=[DataRequired(),  Length(min=3, max=32)])
    father_name = StringField('father_name', validators=[Length(min=3, max=32)])
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
        user = Admin.query.filter_by(first_name=self.first_name.data).first()
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
