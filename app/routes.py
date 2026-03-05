from flask import (
    render_template, redirect, url_for, flash, request, Blueprint, current_app
)
from app import db
from app.forms import SignupForm, LoginForm, BookingForm
from app.models import User, Vehicle, Booking
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlparse as url_parse
from datetime import datetime, date # <-- Added date
from sqlalchemy import and_ # <-- ADDED FOR AVAILABILITY CHECK

bp = Blueprint('routes', __name__)

# --- NEW AVAILABILITY CHECK FUNCTION ---
def is_available(vehicle_id, start_date, end_date):
    """Checks if a vehicle is booked within the given date range."""
    
    # Ensure date objects for comparison
    start_date = date(start_date.year, start_date.month, start_date.day)
    end_date = date(end_date.year, end_date.month, end_date.day)

    # Query for conflicting bookings:
    # A conflict occurs if the new range overlaps an existing booking.
    # The condition is: (Existing end date >= New start date) AND (Existing start date <= New end date)
    
    conflict = Booking.query.filter(
        Booking.vehicle_id == vehicle_id,
        and_(
            Booking.end_date >= start_date,
            Booking.start_date <= end_date
        )
    ).first()
    
    return conflict is None # Returns True if no conflict is found
# --- END NEW FUNCTION ---


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Home')

@bp.route('/vehicles')
def vehicles():
    category = request.args.get('category')
    if category:
        vehicle_list = Vehicle.query.filter_by(category=category).all()
        page_title = f"{category}s"
    else:
        vehicle_list = Vehicle.query.all()
        page_title = "All Vehicles"
    
    return render_template('vehicles.html', title=page_title, vehicles=vehicle_list)

@bp.route('/vehicle/<int:vehicle_id>', methods=['GET', 'POST'])
def vehicle_detail(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    form = BookingForm()
    
    # Pass driver fee to template for JS
    driver_fee = current_app.config['DRIVER_FEE_PER_DAY']

    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        
        # 1. Check User Login
        if not current_user.is_authenticated:
            flash('You must be logged in to make a booking.', 'danger')
            return redirect(url_for('routes.login', next=request.url))
        
        # 2. PERFORM AVAILABILITY CHECK HERE
        if not is_available(vehicle_id, start_date, end_date):
            flash('This vehicle is already booked for part or all of the dates requested.', 'danger')
            # Stay on the same page with the form data
            return render_template('vehicle_detail.html', title=vehicle.name, vehicle=vehicle, form=form, driver_fee=driver_fee)


        # 3. Calculate and Save Booking
        with_driver = form.with_driver.data
        location = form.location.data
        
        # Server-side price calculation
        num_days = (end_date - start_date).days + 1
        base_price = vehicle.price_per_day * num_days
        total_price = base_price
        
        if with_driver:
            total_price += driver_fee * num_days

        booking = Booking(
            start_date=start_date,
            end_date=end_date,
            with_driver=with_driver,
            total_price=total_price,
            location=location,  # Save new location to booking
            customer=current_user,
            vehicle=vehicle
        )
        
        db.session.add(booking)
        db.session.commit()
        
        flash('Your booking has been confirmed!', 'success')
        return redirect(url_for('routes.booking_success'))

    return render_template('vehicle_detail.html', title=vehicle.name, vehicle=vehicle, form=form, driver_fee=driver_fee)

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    form = SignupForm()
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        # Log the user in automatically
        login_user(user)
        
        flash('Congratulations, your account is created and you are now logged in!', 'success')
        # Redirect to the main dashboard
        return redirect(url_for('routes.dashboard'))
        
    return render_template('signup.html', title='Sign Up', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('routes.login'))
        
        login_user(user, remember=form.remember_me.data)
        
        # Handle redirect to 'next' page if user was trying to access a protected route
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('routes.dashboard')
        return redirect(next_page)
        
    return render_template('login.html', title='Login', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.index'))

@bp.route('/dashboard')
@login_required
def dashboard():
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.start_date.desc()).all()
    today = datetime.utcnow().date()  # Get current date
    return render_template('dashboard.html', title='My Dashboard', bookings=bookings, today=today) # Pass date to template

@bp.route('/booking-success')
@login_required
def booking_success():
    return render_template('booking_success.html', title='Booking Successful')

@bp.route('/cancel_booking/<int:booking_id>', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    # Ensure the user owns this booking
    if booking.customer.id != current_user.id:
        flash('You are not authorized to cancel this booking.', 'danger')
        return redirect(url_for('routes.dashboard'))
    
    # Check the 2-day rule
    today = datetime.utcnow().date()
    days_until_start = (booking.start_date - today).days
    
    if days_until_start > 2:
        db.session.delete(booking)
        db.session.commit()
        flash('Your booking has been successfully cancelled.', 'success')
    else:
        flash('Bookings can only be cancelled more than 2 days in advance.', 'danger')
        
    return redirect(url_for('routes.dashboard'))