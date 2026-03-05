from app import db, login_manager  # <-- THIS IS THE FIX
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128))
    
    bookings = db.relationship('Booking', backref='customer', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(100), nullable=False, default='default.jpg')
    price_per_day = db.Column(db.Integer, nullable=False) # In Rupees
    category = db.Column(db.String(50), index=True, nullable=False) # Hatchback, Sedan, SUV, MUV
    passenger_capacity = db.Column(db.Integer, nullable=False)
    fuel_type = db.Column(db.String(20), nullable=False) # Petrol, Diesel, Electric
    
    bookings = db.relationship('Booking', backref='vehicle', lazy='dynamic')

    def __repr__(self):
        return f'<Vehicle {self.name}>'

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    with_driver = db.Column(db.Boolean, default=False)
    location = db.Column(db.String(100), nullable=False)  # <-- Your new location field
    booking_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)

    def __repr__(self):
        return f'<Booking {self.id} for Vehicle {self.vehicle_id}>'