from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User

class SignupForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already in use. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class BookingForm(FlaskForm):
    start_date = DateField('Start Date', validators=[DataRequired()], format='%Y-%m-%d')
    end_date = DateField('End Date', validators=[DataRequired()], format='%Y-%m-%d')
    
    # Your new location dropdown
    location = SelectField(
        'Pickup Location',
        choices=[
            # (Value, Label)
            ('Mumbai - Chhatrapati Shivaji Maharaj Int. Airport', 'Mumbai - Chhatrapati Shivaji Maharaj Int. Airport'),
            ('Delhi - Indira Gandhi Int. Airport', 'Delhi - Indira Gandhi Int. Airport'),
            ('Bengaluru - Kempegowda Int. Airport', 'Bengaluru - Kempegowda Int. Airport'),
            ('Chennai - Chennai Int. Airport', 'Chennai - Chennai Int. Airport'),
            ('Hyderabad - Rajiv Gandhi Int. Airport', 'Hyderabad - Rajiv Gandhi Int. Airport'),
            ('Kolkata - Netaji Subhas Chandra Bose Int. Airport', 'Kolkata - Netaji Subhas Chandra Bose Int. Airport')
        ],
        validators=[DataRequired()]
    )
    
    with_driver = BooleanField('Add a Driver (₹1500/day)')
    submit = SubmitField('Book Now')

    def validate_end_date(self, end_date):
        if end_date.data < self.start_date.data:
            raise ValidationError('End date must be after start date.')