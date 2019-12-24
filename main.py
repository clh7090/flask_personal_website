"""
author: Connor Hunter   <clh7090@rit.edu>

Flask Personal Website
"""


from flask import Flask, redirect, url_for, render_template


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/resume/")
def resume():
    return render_template("resume.html")


if __name__ == "__main__":
    app.run(debug=True)

