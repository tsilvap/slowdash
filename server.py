from flask import Flask, render_template, send_from_directory
app = Flask(__name__, template_folder='./client/dist')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<path:path>')
def send_static(path):
    return send_from_directory('./client/dist', path)
