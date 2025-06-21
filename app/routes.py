from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import RegisterForm, LoginForm

@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}", "success")
        return redirect(url_for("index"))
    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admit@ad.io" and form.password.data == "123":
            flash('Log in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Fail to log in! Check the input', 'danger')
    return render_template("login.html", title="Log In", form=form)
