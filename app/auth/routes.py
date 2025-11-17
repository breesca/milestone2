from flask import Blueprint, render_template, flash, redirect, url_for
from ..forms import LoginForm

auth_bp = Blueprint("auth", __name__, template_folder="templates")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("Not implemented — form validated successfully.", "info")
        return redirect(url_for("main.index"))
    return render_template("auth/login.html", form=form)
