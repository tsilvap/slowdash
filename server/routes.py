from flask import render_template, send_from_directory

from slowdash.slowdash import app


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/<path:path>")
def send_static(path):
    return send_from_directory("./client/dist", path)
