from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
class AddForm(FlaskForm):
    item_id= IntegerField('ID', validators=[DataRequired()])
                          
    name = StringField ('Name', validators=[DataRequired()])
                        
    price= FloatField('Price', validators=[DataRequired()])
    add= SubmitField('Add Product')

class DelForm(FlaskForm):
    item_id= IntegerField('Item ID', validators=[DataRequired()])
    delete= SubmitField('Delete Product')
    
class PurchaseForm(FlaskForm):
    item_id=IntegerField('Item ID', validators=[DataRequired()])
    supplier_id = IntegerField('Supplier ID',validators=[DataRequired()])
    qty= IntegerField('Quantity', validators=[DataRequired()])
    order= SubmitField('Order')
    
    