from . import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Enum
from werkzeug.security import generate_password_hash, check_password_hash

# User Class
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    last_name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    email = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    contact_number = db.Column(db.String(255), nullable=False)
    street_address = db.Column(db.String(100), index=True, nullable=False)  
    # Relationships
    comments = db.relationship('Comment', backref='user', lazy=True)
    orders = db.relationship('Order', backref='user', lazy=True)
    events = db.relationship('Event', backref='organizer', lazy=True)
   
# Event Class
class Event(db.Model):
    __tablename__ = 'events'
    class Status(Enum):
        OPEN = "Open"
        SOLDOUT = "Sold Out"
        CANCELLED = "Cancelled"
        INACTIVE = "Inactive"

        def __str__(self):
            return self.value
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time=db.Column(db.DateTime, nullable =False)
    end_time =db.Column(db.DateTime, nullable = False)
    venue=db.Column(db.String(100), nullable=False)
    ticket_price=db.Column(db.Integer, nullable = False)
    image=db.Column(db.String(400))
    creator_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    ticket_type=db.Column(db.String(20),nullable=False)
    total_ticket=db.Column(db.Integer, nullable =False)
    datetime=db.Column(db.DateTime,)

    

    orders = db.relationship('Order', backref='event', lazy=True)
    comments = db.relationship('Comment', backref='event', lazy=True)
    def __repr__(self):
        return f"Event\nName: {self.name}\nDateTime: {self.datetime}\nVenue: {self.venue}\nTicket Price: {self.ticket_price}\nCreator ID: {self.creator_id}"
    # Foreign Key to reference User who organizes the event
    
    
    # Relationships
    comments = db.relationship('Comment', backref='event', lazy=True)
    orders = db.relationship('Order', backref='event', lazy=True)
    

    
# Comment Class
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(500))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

# Order Class
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(20), nullable=False)
    # Foreign Keys to link to Event and User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    image=db.Column(db.String(400))

# __repr__ Method for Comment (for Debugging Purposes)
def __repr__(self):
    return f"Comment: {self.comment}"