from flask import Blueprint, render_template, redirect
from flask_login import logout_user

user_bp = Blueprint("user", __name__)


@user_bp.route("/register", methods=["GET", "POST"])
def register():
    pass


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    pass


@user_bp.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("#update this"))

