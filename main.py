"""
author: Connor Hunter   <clh7090@rit.edu>

Flask Personal Website
"""


from flask import Flask, request, redirect, url_for, render_template, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "immasecret"
app.permanent_session_lifetime = timedelta(minutes=30)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
database = SQLAlchemy(app)


class Users(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(100), unique=True, nullable=False)
    password = database.Column(database.String(100), unique=True, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.route("/home/", methods=["POST", "GET"])
@app.route("/",  methods=["POST", "GET"])
def home():
    name = ""
    if "name" in session:
        name = session["name"]
        if request.method == "POST":
            name = request.form["nme"]
            password = request.form["pw"]
            session["name"] = name
            session["passwoed"] = password
            existing_user = Users.query.filter_by(username=name).first()
            existing_user.username = name
            existing_user.password = password
            database.session.commit()
        else:
            if "name" in session:
                name = session["name"]
        return render_template("index.html", name=name)
    return render_template("index.html", name=name)


@app.route("/resume/")
def resume():
    if "name" in session:
        name = session["name"]
        return render_template("resume.html", name=name)
    return render_template("resume.html")


@app.route("/login/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        name = request.form["nme"]
        password = request.form["pw"]
        session["password"] = password
        session["name"] = name
        existing_user = Users.query.filter_by(username=name).first()
        if existing_user:
            session["name"] = existing_user.username
            if existing_user.password == session["password"]:
                flash("Login successful.", "info")
                return redirect(url_for("home"))
            else:
                flash("Password is incorrect.", "info")
                session.pop("name", None)
                return redirect(url_for("home"))
        else:
            user = Users(name, password)
            database.session.add(user)
            database.session.commit()
            flash("Account successfully created!", "info")
            return redirect(url_for("home"))
    else:
        if "name" in session:
            flash("You are already logged in.", "info")
            return redirect(url_for("home"))
        return render_template("login.html")


@app.route("/logout/")
def logout():
    if "name" in session and "name" is not None:
        flash("Logout successful.", "info")
        session.pop("name", None)
        return redirect(url_for("home"))
    else:
        flash("You are not logged in.", "info")
        return redirect(url_for("home"))


@app.route("/test_db/")
def test_db():
    return render_template("test_db.html", values=Users.query.all())


if __name__ == "__main__":
    database.create_all()
    app.run(debug=True)
