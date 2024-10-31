from flask import Blueprint, render_template, request, redirect, url_for,flash,current_app
from flask_login import login_required, current_user
from .models import Event,Order, db
from .forms import CreateComment,UpdateEvents
from werkzeug.utils import secure_filename
import os
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
def comment():
    pass

@main_bp.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = UpdateEvents()
    
    if form.validate_on_submit():  # If the form is submitted and valid
        # Grab the creator_id from the currently logged-in user
        creator_id = current_user.id  # get the user id from the session

        image=form.event_image.data # save the image to the server 
        print(type(image))
        filename=secure_filename(image.filename)
        image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        
        # Create the new event instance
        new_event = Event(
            name=form.event_name.data,
            datetime=form.event_datetime.data,
            venue=form.event_venue.data,
            ticket_price=form.event_ticket_price.data,
            genre=form.event_genre.data,
            status="OPEN",
            image=filename,
            creator_id=creator_id
        )
        
        # Add the event to the database
        db.session.add(new_event)
        db.session.commit()
        
        flash('Event created successfully!')
        return redirect(url_for('main.index'))  # Redirect to a suitable page, like the homepage or event list
    
    return render_template('UpdateEvents.html', form=form)  # Render the form template



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
print("main_bp is defined in views.py")