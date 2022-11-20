import os

from flask import Flask
from flask import render_template
from flask import redirect
from flask import request

from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from database import User

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


app = Flask(__name__)

app.config["SECRET_KEY"] = os.urandom(24)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/login")


@login_manager.user_loader
def load_user(id):
    return User.get(id=int(id))


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    name = request.form["name"]
    password = request.form["password"]
    user = User.get(name=name)
    if check_password_hash(user.password, password):
        login_user(user)
        return redirect("/")
    return redirect("/login")


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def register():
    name = request.form["name"]
    password = request.form["password"]
    generate_password_hash(password, method="sha256")
    User.create(
        name=name,
        password=generate_password_hash(password, method="sha256")
        )
    return redirect("/login")


@app.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return redirect("/login")


if __name__ == '__main__':
    app.run(debug=True)
