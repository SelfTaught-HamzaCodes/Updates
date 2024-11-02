from flask import Blueprint, render_template
import json

# Load Dynamic Data:
def load_data():
    with open('data/data.json') as f:
        return json.load(f)

views = Blueprint(__name__, "views")

@views.route("/")
def home():
    data = load_data()
    return render_template("index.html", data=data)

@views.route("/files")
def file_uploads():
    return render_template("files.html")