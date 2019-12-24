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


@app.route("/home/", methods=["POST", "GET"])
@app.route("/",  methods=["POST", "GET"])
def home():
    name = ""
    if "name" in session:
        name = session["name"]
        if request.method == "POST":
            name = request.form["nme"]
            session["name"] = name
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
        session["name"] = name
        flash("Login successful.", "info")
        return redirect(url_for("home"))
    else:
        if "name" in session:
            flash("You are already logged in.", "info")
            return redirect(url_for("home"))
        return render_template("login.html")


@app.route("/logout/")
def logout():
    if "name" in session:
        flash("Logout successful.", "info")
        session.pop("name", None)
        return redirect(url_for("home"))
    else:
        flash("You are not logged in.", "info")
        return redirect(url_for("home"))


@app.route("/test_db/")
def test_db():
    pass


if __name__ == "__main__":
    app.run(debug=True)
