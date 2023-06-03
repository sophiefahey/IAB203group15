from models import Cookuser
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, DateField, TimeField, SubmitField, FileField
from wtforms.validators import DataRequired, EqualTo

# Event creation formSSS
class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    image = FileField('Image')
    description = TextAreaField('Description', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Create Event')

# Comment form
class CommentForm(FlaskForm):
    userid = StringField('userid', validators=[DataRequired()])
    comment = TextAreaField('Comment', validators=[DataRequired()])

# Register form
class RegisterForm(FlaskForm):
    userid = StringField('userid', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), EqualTo('re_password')])
    re_password = PasswordField('re_password', validators=[DataRequired()])

# Login form
class LoginForm(FlaskForm):

    class UserPassword(object):
        def __init__(self, message=None):
            self.message = message

        def __call__(self, form, field):
            userid = form['userid'].data
            password = field.data

            cookuser = Cookuser.query.filter_by(userid=userid).first()
            if cookuser.password != password:
                raise ValueError('Wrong password')
        
            
    userid = StringField('userid', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), UserPassword(message='Wrong password')])

