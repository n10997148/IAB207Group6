from flask import Blueprint, render_template, request, redirect, url_for,flash,current_app
from flask_login import login_required, current_user
from .models import Event,Order, db
from .forms import CreateComment,UpdateEvents
from werkzeug.utils import secure_filename
import os
from datetime import timedelta,datetime

main_bp = Blueprint('main', __name__, template_folder='templates', static_folder='Static')


@main_bp.route('/')
def index(): 
    event = db.session.scalars(db.select(Event)).all()
    return render_template('index.html', event=event)

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
def comment():
    pass

@main_bp.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = UpdateEvents()
    
    if form.validate_on_submit():
        try:
            # Get creator_id from the logged-in user
            creator_id = current_user.id
            event_date = form.date.data
            start_datetime = datetime.combine(event_date, form.start_time.data)
            end_datetime = datetime.combine(event_date, form.end_time.data)
            
            # Handle image upload
            image = form.event_image.data
            filename = secure_filename(image.filename) if image else None
            if filename:
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

            # Create the new event instance
            new_event = Event(
                title=form.event_name.data,
                date=form.date.data,
                start_time=start_datetime,
                end_time=end_datetime,
                venue=form.venue.data,
                description=form.description.data,
                ticket_price=form.ticket_price.data,
                ticket_type=form.ticket_type.data,
                total_ticket=form.total_tickets.data,
                creator_id=creator_id,
                status="OPEN",
                image=filename,
            )

            db.session.add(new_event)
            db.session.commit()
            flash('Event created successfully!')
            return redirect(url_for('main.index'))

        except Exception as e:
            db.session.rollback()
            print("Database commit error:", e)  # Print error if commit fails
            flash('An error occurred while creating the event.')

    else:
        print("Form validation errors:", form.errors)  # Debugging validation issues
    
    return render_template('UpdateEvents.html', form=form)



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

@main_bp.route('/bookings', methods=['GET'])
@login_required
def bookings():
    user_bookings = Order.query.filter_by(user_id=current_user.id).all()  # Retrieve bookings for the current user
    return render_template('Bookings.html', bookings=user_bookings)

print("main_bp is defined in views.py")