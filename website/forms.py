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
    event_name=StringField("Event name", validators=[InputRequired()])
    start_time = TimeField("Start Time", validators=[InputRequired()])
    end_time = TimeField("End Time", validators=[InputRequired()])
    date = DateField("Event Date", validators=[InputRequired()])
    venue = StringField("Venue", validators=[InputRequired()])
    description = StringField("Event Description", validators=[InputRequired()])
    total_tickets = IntegerField("Tickets avaliable", validators=[InputRequired()])
    ticket_type = SelectField("Ticket Type",choices=[("general", "General Admission"), ("vip", "VIP"), ("earlybird", "Early Bird")],validators=[InputRequired()],
    )
    status=SelectField("Select Field",choices=[("open","Open Status"),("sold out", "Sold out Status"),("cancelled","Cancelled Status"),("inactive","Inactive Status")])
    ticket_price=IntegerField("Ticket Price", validators=[InputRequired()])
    event_image=FileField("Image", validators=[DataRequired(), FileAllowed(ALLOWED_FILE, '.jpg & jpeg only!')])
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
    submit = SubmitField("Post")
    
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
    

