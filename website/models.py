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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(400))
    capacity = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    street_address = db.Column(db.String(100), index=True, nullable=False)
    status = db.Column(
        Enum('open', 'inactive', 'sold out', 'cancelled', name='event_status'),
        nullable=False,
        default='open'
    )
    
    # Foreign Key to reference User who organizes the event
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
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
    price = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    
    # Foreign Keys to link to Event and User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)

# __repr__ Method for Comment (for Debugging Purposes)
def __repr__(self):
    return f"Comment: {self.comment}"