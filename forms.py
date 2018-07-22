from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from models import db, User
from flask_wtf.file import FileField, FileAllowed, FileRequired

class SignupForm(Form):
  user_name = StringField('User name', validators=[DataRequired("Please enter your username."),Length(min=6, message="Username must be 6 characters or more.")])
  first_name = StringField('First name', validators=[DataRequired("Please enter your first name.")])
  last_name = StringField('Last name', validators=[DataRequired("Please enter your last name.")])
  email = StringField('Email', validators=[DataRequired("Please enter your email address."), Email("Please enter your email address.")])
  password = PasswordField('Password', validators=[DataRequired("Please enter a password."), Length(min=8, message="Passwords must be 8 characters or more.")])
  submit = SubmitField('Sign up')

  def validate_user_name(self, field):
        user = User.query.filter(User.username == self.user_name.data).first()
        if user:
            raise ValueError("Sorry.. Username exists")
    
class LoginForm(Form):
  user_name = StringField('User name', validators=[DataRequired("Please enter your username.")])
  password = PasswordField('Password', validators=[DataRequired("Please enter a password.")])
  submit = SubmitField("Sign in")

class ForgotPassword(Form):
  user_name = StringField('User name', validators=[DataRequired("Please enter your username.")])
  submit = SubmitField("Enter")

class AddImage(Form):
    user_image = FileField('User Image', validators=[FileRequired()]) #, FileAllowed(user_image, 'Images only!')
    submit = SubmitField("Upload")