import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect
from forms import RegisterForm, LoginForm

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    form = RegisterForm()
    return render_template("register.html", title="Register", form=form)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", title="Log In", form=form)









if __name__ == "__main__":
    app.run(debug=True)