"""
author: Connor Hunter   <clh7090@rit.edu>

Flask Personal Website
"""


from flask import Flask, request, redirect, url_for, render_template, session
from datetime import timedelta


app = Flask(__name__)
app.secret_key = "immasecret"
app.permanent_session_lifetime = timedelta(days=1)


@app.route("/home/")
@app.route("/")
def home():
    if "name" in session:
        name = session["name"]
        return render_template("index.html", name=name)
    return render_template("index.html")


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
        return redirect(url_for("user"))
    else:
        if "name" in session:
            return redirect(url_for("user"))
        return render_template("login.html")


@app.route("/user")
def user():
    if "name" in session:
        name = session["name"]
        return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("name", None)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)

