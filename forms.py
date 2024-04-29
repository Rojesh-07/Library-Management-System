from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from LMS.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class addbookForm(FlaskForm):
    book_name = StringField('Book Name',
                           validators=[DataRequired(), Length(min=2, max=100)])
    content = TextAreaField('Content',
                        validators=[DataRequired(), Length(min=2, max=2000)])
    author_name = StringField('Author Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    image_file = FileField('Update Profile Picture',
                           validators=[FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField('Add Book')

class Search(FlaskForm):
    book_name = StringField('Book Name',
                            validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Search')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired(),Length(min=2 , max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])

    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png','jpeg'])])

    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user=User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is Taken! Please Choose a different one.')
        
    def validate_email(self, email):
        if email.data != current_user.email:
            user=User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That Email is Taken! Please Choose a different one.')
            


    


