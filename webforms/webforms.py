from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField
from wtforms.fields import DateField

# Create a Form Class
class UserName(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    birth_date = DateField('Birth Date', format='%Y-%d-%m')
    city = StringField('City')
    about_author = TextAreaField('About Author')
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match!')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    profile_picture = FileField('Profil Picture')
    submit = SubmitField('Submit')


# Create A Password Form Class
class PasswordForm(FlaskForm):
    email = StringField("What's Your Email:", validators=[DataRequired()])
    password_hash = PasswordField("What's Your Password:", validators=[DataRequired()])
    submit = SubmitField('Submit')


# Create A Login Form Class
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


# Create A User Form Class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    birth_date = DateField('Birth Date', format='%Y-%d-%m')
    city = StringField("City")
    about_author = TextAreaField("About Author")
    password_hash = PasswordField("Password", validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match!')])
    password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])
    profil_picture = FileField("Profile Picture")
    submit = SubmitField("Submit")    


# Create A Search Form Class
class SearchForm(FlaskForm):
    searched = StringField('Searched', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Create A Post Form Class
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = CKEditorField('Content', validators=[DataRequired()])
    author = StringField('Author')
    slug = StringField('Slug', validators=[DataRequired()])
    submit = SubmitField('Submit')