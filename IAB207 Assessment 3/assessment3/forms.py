from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo

#Create new event
class EventForm(FlaskForm):
  name = StringField('Event Name', validators=[InputRequired()])
  image = StringField('Cover Image', validators=[InputRequired()])
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