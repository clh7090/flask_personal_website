"""
author: Connor Hunter   <clh7090@rit.edu>

Flask Personal Website
"""


from datetime import timedelta
from flask import Flask, request, redirect, url_for, render_template, session, flash  # Must be installed
from flask_sqlalchemy import SQLAlchemy  # Must be installed


app = Flask(__name__)
app.secret_key = "immasecret"
app.permanent_session_lifetime = timedelta(minutes=30)  # 30 minute sessions
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
database = SQLAlchemy(app)


class Users(database.Model):
    """
    Each user has a username and password, with a list of notes, if they decide to make some
    """
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(10), unique=True, nullable=False)
    password = database.Column(database.String(10), nullable=False)
    notes = database.relationship("Notes", backref="owner", cascade="delete-orphan")  # Each user has a list of notes
    # The delete orphan IS VERY IMPORTANT

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Notes(database.Model):
    """
    Each Note belongs to a user, a user may have multiple notes
    """
    id = database.Column(database.Integer, primary_key=True)
    notes = database.Column(database.String(150), nullable=False)
    owner_id = database.Column(database.Integer, database.ForeignKey("users.id"), nullable=False)

    def __init__(self, notes, owner):
        self.notes = notes
        self.owner = owner  # refers to the User class


@app.route("/test_db/")  # Collects all data on users and their notes
def test_db():
    return render_template("test_db.html", users=Users.query.all(), notes=Notes.query.all())



@app.route("/home/")
@app.route("/")
def home():
    name = ""
    if "name" in session:  # logged in
        name = session["name"]
        return render_template("index.html", name=name)  # just going to home with a get request
    return render_template("index.html", name=name)  # no name, not logged in


@app.route("/resume/")
def resume():
    if "name" in session:  # logged in
        name = session["name"]
        return render_template("resume.html", name=name)
    return render_template("resume.html")  # no name


@app.route("/login/", methods=["POST", "GET"])
def login():
    if request.method == "POST":  # logging in
        session.permanent = True
        name = request.form["nme"]  # login.html
        password = request.form["pw"]  # login.html
        session["password"] = password
        session["name"] = name
        existing_user = Users.query.filter_by(username=name).first()
        if existing_user:  # in the database
            session["name"] = existing_user.username
            if existing_user.password == session["password"]:  # Correct password
                flash("Login successful.", "info")
                return redirect(url_for("home"))
            else:
                flash("Password is incorrect.", "info")  # Incorrect password
                session.pop("name", None)  # essentially logged out, must have a name to view private things
                return redirect(url_for("home"))
        else:
            new_user = Users(name, password)  # Creates a new user since one doesn't exist with that username
            database.session.add(new_user)
            database.session.commit()  # storing in db
            flash("Account successfully created!", "info")
            return redirect(url_for("home"))
    else:
        if "name" in session: # already logged in
            flash("You are already logged in.", "info")
            return redirect(url_for("home"))
        return render_template("login.html")  # not logged in yet, about to send a get/post request to the server.


@app.route("/logout/")
def logout():
    if "name" in session:  # Can logout since you're logged in
        flash("Logout successful.", "info")
        session.pop("name", None)  # essentially logged out, must have a name to view private things
        return redirect(url_for("home"))
    else:
        flash("You are not logged in.", "info")  # Cannot logout since you're not logged in
        return redirect(url_for("home"))


@app.route("/notes/")
def notes():
    if "name" in session:  # Must be logged in
        name = session["name"]
        existing_user = Users.query.filter_by(username=name).first()
        my_note = existing_user.notes  # list of notes
        return render_template("notes.html", name=name, note_list=my_note)
    flash("You must log in to see sticky notes.", "info")
    return render_template("index.html")


@app.route("/add/", methods=["POST"])
def add_note():
    if request.method == "POST":
        name = session["name"]
        existing_user = Users.query.filter_by(username=name).first()
        my_note = existing_user.notes  # list of notes
        if len(my_note) <= 5:
            text = request.form["nte"]
            new_note = Notes(notes=text, owner=existing_user)
            database.session.add(new_note)  # comitting the note, with the user as whoever is logged in
            database.session.commit()
            return render_template("notes.html", name=name, note_list=my_note)
        flash("You must delete an old note first.", "info")
        return render_template("notes.html", name=name, note_list=my_note)


@app.route("/del/", methods=["POST"])
def del_note():
    if request.method == "POST":
        name = session["name"]
        existing_user = Users.query.filter_by(username=name).first()
        my_note = existing_user.notes
        my_note[:] = my_note[:-1]  # deletes the last note on the pile, the one that was added first
        database.session.commit()
        return render_template("notes.html", name=name, note_list=my_note)


if __name__ == "__main__":
    database.create_all()
    app.run()

