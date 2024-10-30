from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Event,Order, db

main_bp = Blueprint('main', __name__, template_folder='templates', static_folder='Static')


@main_bp.route('/')
def index(): 
    return render_template('index.html')

@main_bp.route('/view_event', methods=['GET'])
def view_event():
    return render_template('EventDetails.html')

@main_bp.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    if request.method == 'POST':
        title = request.form.get('eventName')
        description = request.form.get('eventDescription')
        date = request.form.get('eventDate')

     


        # Create new event
        new_event = Event(title=title, description=description, date=date, status='Open')
        db.session.add(new_event)
        db.session.commit()

        return redirect(url_for('INDEX'))
    
    return render_template('UpdateEvents.html')

@main_bp.route('/order', methods=['GET', 'POST'])
def order():
    events = Event.query.filter_by(status='Open').all()  
    
    if request.method == 'POST':
        event_id = request.form.get('selectEvent')
        quantity = request.form.get('ticketQuantity')
        
        
            
            # Create new booking
        new_booking = order(quantity=quantity, price=price, user_id=current_user.id, event_id=event_id)
        db.session.add(new_booking)
        db.session.commit()


        return redirect(url_for('index'))

    return render_template('Bookings.html', events=events)
print("main_bp is defined in views.py")