from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG', 'JPG', 'png', 'jpg'}

#Create Login Form
class LoginForm(FlaskForm):
    emailid=StringField("Email Address", validators=[InputRequired('Enter your Email Address')])
    password=PasswordField("Password", validators=[InputRequired('Enter your Password')])
    submit = SubmitField("Login")

 # Create registration form
class RegisterForm(FlaskForm):
    FirstName=StringField("First Name", validators=[InputRequired()])
    LastName=StringField("Lirst Name", validators=[InputRequired()])    
    emailid = EmailField("Email Address", validators=[Email("Please enter a valid email")])
    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired()])
    confirm=PasswordField("Confirm Password", validators=[InputRequired()])
    contactNumber = StringField("Contact Number", validators=[InputRequired()])
    address =StringField("Address of Residence", validators=[InputRequired()])
    #submit button
    submit = SubmitField("Register")
    
#Create new event
class EventForm(FlaskForm):
  name = StringField('Event Name', validators=[InputRequired()])
  image = FileField('Cover Image', validators=[FileRequired(message = 'Image cannot be empty'), FileAllowed(ALLOWED_FILE, message = 'Only supports PNG, JPG, png, jpg')])
  description = TextAreaField('Description', validators=[InputRequired()])
  date = StringField('Event Date', validators=[InputRequired()])
  time = StringField('Event Time', validators=[InputRequired()])
  location = StringField('Event Location', validators=[InputRequired()])
  category = StringField('Event Category', validators=[InputRequired()])
  submit = SubmitField("Create")

  


#User comment
class CommentForm(FlaskForm):
  text = TextAreaField('Comment', [InputRequired()])
  submit = SubmitField('Create')
