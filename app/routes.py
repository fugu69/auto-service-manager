import os
import secrets
from PIL import Image
from flask import render_template, flash, redirect, url_for, request, abort
from app import app, db, bcrypt
from app.forms import RegisterForm, LoginForm, UpdateAccountForm, AddVehicleForm, UpdateVehicleForm
from app.models import User, Vehicle
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlparse, urljoin

# Helper function to check if the redirect target is safe
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created! You can LOG IN now", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    next_page = request.args.get('next')

    # Treat empty string or literal "None" as no redirect
    if not next_page or next_page.lower() == "none":
        next_page = None

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            # GET or POST value
            post_next = request.form.get('next') or next_page
            safe_next = post_next if post_next and is_safe_url(post_next) else None

            return redirect(safe_next or url_for("index"))

        flash('Fail to log in! Check the input', 'danger')

    return render_template("login.html", title="Log In", form=form, next_page=next_page)




@app.route("/logout", methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_file_name = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_file_name)
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_file_name


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + (current_user.image_file or 'default.jpg'))
    return render_template("account.html", title="Account", image_file=image_file, form=form)

@app.route("/vehicle/new", methods=['GET', 'POST'])
@login_required
def new_vehicle():
    form = AddVehicleForm()
    if form.validate_on_submit():
        vehicle = Vehicle(make=form.make.data, model=form.model.data, year=form.year.data, mileage=form.mileage.data, owner=current_user)
        db.session.add(vehicle)
        db.session.commit()
        flash("Car added to the garage!", "success")
        return redirect(url_for('garage'))
    return render_template("add_vehicle.html", title="New Vehicle", 
                           legend="Add New Vehicle", form=form)

@app.route("/vehicle/<int:vehicle_id>")
@login_required
def vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    return render_template("vehicle.html", title=f"{vehicle.make} {vehicle.model}", vehicle=vehicle)

@app.route("/vehicle/<int:vehicle_id>/update", methods=['GET', 'POST'])
@login_required
def update_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    if vehicle.owner != current_user:
        abort(403)
    form = UpdateVehicleForm(obj=vehicle)
    if form.validate_on_submit():
        vehicle.make = form.make.data
        vehicle.model = form.model.data
        vehicle.year = form.year.data
        vehicle.mileage = form.mileage.data
        db.session.commit()
        flash("Vehicle Info has been updated", "success")
        return redirect(url_for("vehicle", vehicle_id=vehicle.id))

    return render_template("update_vehicle.html", title="Update Vehicle",
                           legend="Update Vehicle Info", form=form)

@app.route("/garage", methods=['GET', 'POST'])
@login_required
def garage():
    vehicles = Vehicle.query.filter_by(user_id=current_user.id).all()
    return render_template("garage.html", title="Garage", vehicles=vehicles)