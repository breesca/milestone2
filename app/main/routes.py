from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ..models import Goal

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return render_template("main/index.html", title="Home")

@main_bp.route("/feature")
def feature():
    return render_template("main/feature.html", title="Feature Demo")

@main_bp.route("/dashboard")
@login_required
def dashboard():
    goals = Goal.query.filter_by(user_id=current_user.id).all()
    return render_template("main/dashboard.html", goals=goals, title="Dashboard")

