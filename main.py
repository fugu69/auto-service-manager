from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def index():
    return "Test123"

@app.route("/register")
def register():
    return "Register page"

@app.route("/login")
def login():
    return "Login page"









if __name__ == "__main__":
    app.run(debug=True)