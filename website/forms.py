from flask_wtf import FlaskForm
from wtforms.fields import (
    TextAreaField,
    SubmitField,
    StringField,
    PasswordField,
    IntegerField,
    TimeField,
    DateField,
    DateTimeLocalField,
    SelectField,
    DateTimeField,
)
from wtforms.validators import InputRequired, Length, Email, EqualTo, DataRequired

from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'png', 'jpg', 'JPG', 'PNG', 'bmp'}

class UpdateEvents(FlaskForm): # This form is for creating events
    Start_time = TimeField("Start Time", validators=[InputRequired()])
    date = DateField("Event Date", validators=[InputRequired()])
    Venue = StringField("Venue", validators=[InputRequired()])
    Category = StringField("User Name", validators=[InputRequired()])
    Tickets_avaliable = IntegerField("Tickets avaliable", validators=[InputRequired()])
    status = StringField("User Name", validators=[InputRequired()])
    
    event_image=FileField("Image", validators=[DataRequired(), FileAllowed(['jpg'], '.jpg only!')])
    create_event=SubmitField("Create Event")
    
class CreateUser(FlaskForm):
    """
        A form for creating users
    """
    name = StringField("Name", validators=[InputRequired()])
    emailid = StringField("Email", validators=[InputRequired()])
    password_hash = StringField("Password", validators=[InputRequired()])
    
    
class CreateComment(FlaskForm):
    """
        A form for creating a comment
    """
    comment = StringField("Comment", validators=[InputRequired()])
    submit = SubmitField("Create")
    
# creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password_hash=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

# this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    email = StringField("Email Address", validators=[Email("Please enter a valid email")])
    # linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    contact_number=StringField("Contact Number", validators=[InputRequired()])
    street_address=StringField("Street Address", validators=[InputRequired()])

    # submit button
    submit = SubmitField("Register")
    

