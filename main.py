from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html", title="Register")

@app.route("/login")
def login():
    return render_template("login.html", title="Log In")









if __name__ == "__main__":
    app.run(debug=True)