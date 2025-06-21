from app import db
from datetime import datetime, timezone

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    license_start_date = db.Column(db.Date)
    license_end_date = db.Column(db.Date)
    license_scan_path = db.Column(db.String(255))

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # link to owner
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    mileage = db.Column(db.Integer, nullable=False)
    vin = db.Column(db.String(17), unique=True)
    color = db.Column(db.String(30))
    engine_type = db.Column(db.String(50))
    engine_model = db.Column(db.String(50))
    engine_number = db.Column(db.String(50))
    transmission_type = db.Column(db.String(50))
    transmission_model = db.Column(db.String(20))

    # Tax
    tax_start_date = db.Column(db.Date)
    tax_end_date = db.Column(db.Date)

    # Insurance
    insurance_start_date = db.Column(db.Date)
    insurance_end_date = db.Column(db.Date)

    # Scans (store as file paths or URLs to uploads)
    registration_scan_path = db.Column(db.String(255))
    insurance_scan_path = db.Column(db.String(255))

    maintenance = db.relationship('MaintenanceRecord', backref='vehicle', lazy=True)

class MaintenanceRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    service_type = db.Column(db.String(100), nullable=False)
    service_date = db.Column(db.Date, nullable=False)
    mileage_at_service = db.Column(db.Integer)
    notes = db.Column(db.Text)
    part_number = db.Column(db.String(50))
    part_name= db.Column(db.String(50))
    part_cost= db.Column(db.Float)
    parts_cost = db.Column(db.Float)
    service_cost = db.Column(db.Float)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class MaintenanceSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    service_type = db.Column(db.String(100), nullable=False)
    interval_miles = db.Column(db.Integer)  # e.g., 5000
    last_service_mileage = db.Column(db.Integer)
    next_due_mileage = db.Column(db.Integer)
    due_date = db.Column(db.Date)
