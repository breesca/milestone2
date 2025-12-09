from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from ..models import Goal
from ..forms import GoalForm

main_bp = Blueprint("main", __name__, template_folder="../templates")

@main_bp.route("/")
def index():
    return render_template("main/index.html", title="Home")

@main_bp.route("/feature")
def feature():
    return render_template("main/feature.html", title="Feature Demo")

@main_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    form = GoalForm()
    if form.validate_on_submit():
        goal = Goal(
            title=form.title.data,
            week=form.week.data,
            owner=current_user,
        )
        from .. import db
        db.session.add(goal)
        db.session.commit()
        return redirect(url_for("main.dashboard"))

    goals = Goal.query.filter_by(user_id=current_user.id).all()
    return render_template("main/dashboard.html", goals=goals, form=form, title="Dashboard")

