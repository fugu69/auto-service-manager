from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime, timezone

"""
If you ever get stuck again with PostgreSQL users/roles, just remember: DB ownership, 
schema ownership, and GRANTs are three separate things that all need to be aligned.
1. Database Ownership
ALTER DATABASE your_db_name OWNER TO your_user;
2. Schema Ownership
ALTER SCHEMA public OWNER TO your_user;
3. Privileges (GRANTs)
Grant specific permissions like CREATE, USAGE, SELECT, INSERT, etc.
GRANT CREATE, USAGE ON SCHEMA public TO your_user;
GRANT CONNECT ON DATABASE your_db_name TO your_user;

Why All Three Matter
If database ownership is missing, user might not be able to connect or manage the database.

If schema ownership or privileges are missing, the user cannot create or modify tables inside that schema.

If GRANT permissions are missing, the user might connect but will get permission errors when creating or querying tables.

---

user.vehicles → list all vehicles owned by a user

vehicle.owner → get the user that owns a vehicle

vehicle.maintenance_records → get all maintenance done

vehicle.maintenance_schedules → upcoming scheduled maintenance

record.vehicle.make → get which car was serviced
"""

from datetime import datetime, timezone

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    license_start_date = db.Column(db.Date)
    license_end_date = db.Column(db.Date)
    license_scan_path = db.Column(db.String(255))

    # One-to-many: User → Vehicle
    vehicles = db.relationship('Vehicle', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Tax and insurance
    tax_start_date = db.Column(db.Date)
    tax_end_date = db.Column(db.Date)
    insurance_start_date = db.Column(db.Date)
    insurance_end_date = db.Column(db.Date)

    # File paths
    registration_scan_path = db.Column(db.String(255))
    insurance_scan_path = db.Column(db.String(255))

    # One-to-many: Vehicle → MaintenanceRecord
    maintenance_records = db.relationship('MaintenanceRecord', backref='vehicle', lazy=True)

    # One-to-many: Vehicle → MaintenanceSchedule
    maintenance_schedules = db.relationship('MaintenanceSchedule', backref='vehicle', lazy=True)

    def __repr__(self):
        return f"Vehicle('{self.make}', '{self.model}', {self.year})"


class MaintenanceRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)

    service_type = db.Column(db.String(100), nullable=False)
    service_date = db.Column(db.Date, nullable=False)
    mileage_at_service = db.Column(db.Integer)
    notes = db.Column(db.Text)

    # Optional part info
    part_number = db.Column(db.String(50))
    part_name = db.Column(db.String(50))
    part_cost = db.Column(db.Float)
    parts_cost = db.Column(db.Float)
    service_cost = db.Column(db.Float)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<MaintenanceRecord({self.service_type}, {self.service_date})>"


class MaintenanceSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)

    service_type = db.Column(db.String(100), nullable=False)
    interval_miles = db.Column(db.Integer)
    last_service_mileage = db.Column(db.Integer)
    next_due_mileage = db.Column(db.Integer)
    due_date = db.Column(db.Date)

    def __repr__(self):
        return f"<Schedule({self.service_type}, next due at {self.next_due_mileage} miles)>"

