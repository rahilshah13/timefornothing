from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from breeze.models import User
from breeze.models import Email as gmail

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=50)])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=6, max=50), EqualTo('password')])

	submit = SubmitField('Sign Up') 

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('That username is taken.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('That email is in use.')

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=50)])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[])
    comic = FileField('Upload Comic', validators=[DataRequired(), FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post')


class EmailForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Sign Up') 

	def validate_email(self, email):
		em = gmail.query.filter_by(email=email.data).first()
		if em:
			raise ValidationError('That email has already been used.')

