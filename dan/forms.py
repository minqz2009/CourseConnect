from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, RadioField, DateTimeField, SelectField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length, Email, EqualTo, NumberRange
from dan.models import User

class LoginForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    email = StringField('Email', validators=[DataRequired(), Email()])

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register New User')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Email already registered")

class ReviewForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    review = TextAreaField('Review', validators=[DataRequired()])
    rating = IntegerField('Rating', validators=[NumberRange(min=0, max=5)])
    user_grade = IntegerField('Your Grade', validators=[NumberRange(min=0, max=100)])
    submit = SubmitField('Add Review') 

class CourseSearchForm(FlaskForm):
    search = StringField('Search')
    submit = SubmitField('Search')
    course = SelectField('Course Type', choices=[('0', ''), ('COMP', 'COMP'), ('MATH', 'MATH'), ('ELEC', 'ELEC'), ('MATH', 'MATH')])
 
