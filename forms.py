from models import Cookuser, Event
from flask_wtf import FlaskForm
from wtforms import SelectField, FileField, StringField, TextAreaField, PasswordField, DateField, TimeField, SubmitField, IntegerField, EmailField
from wtforms.validators import DataRequired, EqualTo

# Event creation formSSS
class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    image = FileField('Image')
    description = TextAreaField('Description', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    address = StringField('Location', validators=[DataRequired()]) 
    postgraduate = IntegerField('Postgraduate',validators=[DataRequired()])
    student =  IntegerField('Student',validators=[DataRequired()])
    concession = IntegerField('Concession',validators=[DataRequired()])
    submit = SubmitField('Create Event')
    dropdown_list = ['IT', 'Nursing', 'Engineering', 'Arts', 'Education', 'Business'] 
    category = SelectField('Category', choices=dropdown_list, default=1)
    status_list = ['Open', 'SoldOut', 'Inactive', 'Cancelled'] 
    status = SelectField('Status', choices=status_list, default=1)
    states_list = ['NSW', 'NT', 'QLD', 'SA', 'TA', 'VIC', 'WA']
    states = SelectField('State', choices=states_list, default=1)

# Comment form
class CommentForm(FlaskForm):
    id = StringField('userid', validators=[DataRequired()])
    title = TextAreaField('comment', validators=[DataRequired()])
    created_at = DateField ('created_at', validators=[DataRequired()])

# Register form
class RegisterForm(FlaskForm):
    userid = StringField('userid', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    phonenumber = StringField('phone number', validators=[DataRequired()])
    address = StringField('address', validators=[DataRequired()])
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

#Booking Form
class BookingForm(FlaskForm):
    booked_student = SelectField("Test: ", choices=[(-1, "0"), (1, "1"), (2, "2"),(3, "3"), (4, "4"), (5, "5"),(6,"6")])
    booked_postgraduate = SelectField("Test: ", choices=[(-1, "0"), (1, "1"), (2, "2"),(3, "3"), (4, "4"), (5, "5"),(6,"6")])
    booked_concession = SelectField("Test: ", choices=[(-1, "0"), (1, "1"), (2, "2"),(3, "3"), (4, "4"), (5, "5"),(6,"6")])
    submit = SubmitField('Book Event')

