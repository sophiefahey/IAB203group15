from flask import Blueprint, render_template, request
from flask import session

viewsbp = Blueprint('main',__name__)

@viewsbp.route("/")
def index():
    return render_template("index.html")