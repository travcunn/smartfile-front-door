from flask_wtf import Form
from wtforms import PasswordField, TextField
from wtforms.fields import BooleanField
from wtforms.validators import DataRequired


class LoginForm(Form):
    username = TextField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')


class DeleteUserForm(Form):
    pass


class CreateUserForm(Form):
    first_name = TextField('First Name', validators=[DataRequired()])
    last_name = TextField('Last Name', validators=[DataRequired()])
    username = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password')
