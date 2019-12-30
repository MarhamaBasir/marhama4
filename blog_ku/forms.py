from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
# TextAreaField add in p.10
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from blog_ku.models import User
from flask_login import current_user #add in p.9
from flask_wtf.file import FileField, FileAllowed #add in p.9


class Registrasi_F(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	konfirmasi_password = PasswordField('Konfirmasi_Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField ('Sign Up')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username yang anda masukan sudah digunakan, cobalah menggunakan username yang berbeda')
	
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email yang anda masukan sudah digunakan, cobalah menggunakan email yang berbeda')
			
	def validate_password(self, password):
		user = User.query.filter_by(password=password.data).first()
		if user:
			raise ValidationError('Password yang anda masukan sudah digunakan, cobalah menggunakan username yang berbeda')

class Login_F(FlaskForm):
	email = StringField ('Email', validators=[DataRequired(), Email()])
	password = PasswordField ('Password', validators=[DataRequired()])
	remember= BooleanField('Remember Me')
	submit = SubmitField ('Login')


# ===================BATAS loginadmin========================
class Loginadmin_F(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	password = PasswordField ('Password', validators=[DataRequired()])
	remember= BooleanField('Remember Me')
	submit = SubmitField ('Login')

class Update_Account_F(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	foto = FileField('Update Foto Profil', validators=[FileAllowed(['jpg','png'])])
	submit=SubmitField('Update')

	def validate_username(self, username):
		if username.data != current_user.username:
		# if username.data !=current_user.emaildbw:
			user = User.query.filter_by(username=username.data). first()
			if user:
				raise ValidationError('Username yang anda masukan sudah digunakan, cobalah menggunakan username yang berbeda')

	def validate_emial(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data). first()
			if user:
				raise ValidationError('Email yang anda masukan sudah digunakan, cobalah menggunakan email yang berbeda')

# =============add in p.10==============
class Post_F(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	konten = TextAreaField('konten', validators=[DataRequired()])
	submit = SubmitField('POST')
