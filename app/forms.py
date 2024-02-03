from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Edit Profile')


class LoginForm(FlaskForm):
    '''LoginForm'''
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    '''RegisterForm'''
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(' Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')
    
class PostForm(FlaskForm):
    """ Comment Form """
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Post')