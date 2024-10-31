from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Event,Order, db
from .forms import CreateComment
from datetime import timedelta

main_bp = Blueprint('main', __name__, template_folder='templates', static_folder='Static')


@main_bp.route('/')
def index(): 
    events = db.session.scalars(db.select(Event)).all()
    return render_template('index.html', events=events)

@main_bp.route('/search')
def search():
    if request.args['search'] and request.args['search'] != "":
        print(request.args['search'])
        query = "%" + request.args['search'] + "%"
        events = db.session.scalars(db.select(Event).where(Event.description.like(query)))
        return render_template('index.html', events=events)
    else:
        return redirect(url_for('main.index'))


@main_bp.route('/view_event/<current_event_id>')
def view_event(current_event_id):
    current_event = db.session.scalar(db.select(Event).where(Event.id==current_event_id))
    print(current_event_id, current_event.name)
    cForm = CreateComment()
    return render_template('EventDetails.html', event=current_event, form=cForm)

@main_bp.route('/view_event/<current_event_id>/comment', methods=['GET', 'POST'])
def comment(current_event_id):
    # Implement comment functionality here
    pass

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
        price = request.form.get('price')
        
            
            # Create new booking
        new_booking = order(quantity=quantity, price=price, user_id=current_user.id, event_id=event_id)
        db.session.add(new_booking)
        db.session.commit()


        return redirect(url_for('index'))

    return render_template('Bookings.html', events=events)

@main_bp.route('/bookings')
@login_required
def bookings():
    orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template('Bookings.html', orders=orders)

print("main_bp is defined in views.py")