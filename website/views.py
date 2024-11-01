from flask import Blueprint, render_template, request, redirect, url_for,flash,current_app,abort
from flask_login import login_required, current_user
from .models import User,Event,Order, db, Comment
from .forms import CreateComment,UpdateEvents,OrderForm
from werkzeug.utils import secure_filename
import os
from datetime import timedelta,datetime

main_bp = Blueprint('main', __name__, template_folder='templates', static_folder='Static')


@main_bp.route('/')
def index(): 
    event= Event.query.all()
    event = db.session.scalars(db.select(Event)).all()
    return render_template('index.html', event=event)

@main_bp.route('/search')
def search():
    if request.args['search'] and request.args['search'] != "":
        print(request.args['search'])
        query = "%" + request.args['search'] + "%"
        events = db.session.scalars(db.select(Event).where(db.or_(Event.name.ilike(query),
                    Event.description.ilike(query))))
        return render_template('index.html', event=events)
    else:
        return redirect(url_for('main.index'))


@main_bp.route('/show/<int:id>', methods=['GET', 'POST'])
def show(id):
    # Fetch the event using the provided ID
    event = db.session.scalar(db.select(Event).where(Event.id == id))

    # Retrieve comments only for this event
    comments = db.session.scalars(db.select(Comment).where(Comment.event_id == id)).all()

    # Initialize the comment and booking forms
    cform = CreateComment()
    oform = OrderForm()


    if cform.validate_on_submit():
        # Process the comment form
        user_id = current_user.id
        new_comment = Comment(
            text=cform.comment_text.data,
            created_at=datetime.now(),
            user_id=user_id,
            event_id=event.id 
        )
        db.session.add(new_comment)
        db.session.commit()
        flash("Comment added successfully!", "success")
        return redirect(url_for('event.show', id=event.id))

    if oform.validate_on_submit():
        # Process the booking form
        user_id = current_user.id
        ticket_type = request.form.get('total_tickets')
        new_order = Order(
            quantity=oform.total_tickets.data,
            type=ticket_type,
            user_id=user_id,
            event_id=event.id
        )
        db.session.add(new_order)
        db.session.commit()
        flash("Order placed successfully!", "success")
        return redirect(url_for('main.show', id=event.id))
    return render_template('EventDetails.html', event=event, comments=comments, form=cform, oform=oform)

@main_bp.route('/view_event/<event_id>/comment', methods=['GET', 'POST'])
def comment(event_id):
    form = CreateComment()  
    # get the event object associated to the page and the comment
    event = db.session.scalar(db.select(Event).where(Event.id==event_id))  
    if form.validate_on_submit():
      if current_user:
        # read the comment from the form
        comment = Comment(comment=form.comment.data, event=event, user=current_user) 
        # here the back-referencing works - comment.event is set
        # and the link is created
        db.session.add(comment) 
        db.session.commit() 

        # flashing a message which needs to be handled by the html
        # flash('Your comment has been added', 'success')  
        print('Your comment has been added', 'success')
    # using redirect sends a GET request to view_event
    return redirect(url_for('main.show', id = event_id))

@main_bp.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = UpdateEvents()
    
    if form.validate_on_submit():
        try:
            creator_id = current_user.id
            event_date = form.date.data
            start_datetime = datetime.combine(event_date, form.start_time.data)
            end_datetime = datetime.combine(event_date, form.end_time.data)# Set up the event data
            image = form.event_image.data
            filename = secure_filename(image.filename) if image else None
            if filename:
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

            new_event = Event(
                name=form.event_name.data,
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

            print("New Event Data:", new_event)  # Print to confirm data assignment
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




@main_bp.route('/order', methods=['GET','POST'])
@login_required
def order():
    form = OrderForm()
    
    if form.validate_on_submit():
        user_id = current_user.id
        new_order = Order(
            total_tickets=form.ticket_total_tickets.data,
            type=form.ticket_type.data,
            user_id=current_user.id,
            event_id=form.event_id.data,
            image=db.session.scalar(db.select(Event.image).where(Event.id == form.event_id.data))
        )

        db.session.add(new_order)
        db.session.commit()
        flash("order placed", "success")
    return render_template("EventDetails.html", form=form)


@main_bp.route('/bookings')
@login_required
def bookings():
    orders = Order.query.filter_by(user_id=current_user.id).join(Event, Order.event_id == Event.id).add_columns(
    Order.id.label('order_id'),
    Order.quantity,
    Order.type,
    Order.event_id,
    Order.image,
    )
    return render_template('Bookings.html', orders=orders)

print("main_bp is defined in views.py")