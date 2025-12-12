from flask import current_app, jsonify, Blueprint, render_template

home_bp = Blueprint('home_controller', __name__)

@home_bp.route('/')
def home():
    return render_template("home.html")