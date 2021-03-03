from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import (
    logout_user,
    login_user,
    login_required,
    current_user,
)
from todo.models import User, Todo
from todo.forms import RegisterForm, LoginForm
from todo.extensions import db, login_manager, csrf

user_bp = Blueprint("user", __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    # store the url they were trying to visit in the session
    session["after_login"] = request.url
    flash("You need to login", "warning")
    return redirect(url_for("user.login"))


@user_bp.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        flash("You are already logged in", "warning")
        return redirect(url_for("landing.index"))

    form = RegisterForm()
    if form.validate_on_submit():

        user = User(username=form.username.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()
        login_user(user)

        flash("Registered successfully", "success")

        return redirect(url_for("landing.index"))

    return render_template("users/register.html", form=form)


@user_bp.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        flash("You are already logged in", "warning")
        return redirect(url_for("landing.index"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        login_user(user)
        return redirect(session.get("after_login") or url_for("landing.index"))

    return render_template("users/login.html", form=form)


@user_bp.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("landing.index"))


@user_bp.route("/delete", methods=["POST"])
@login_required
@csrf.exempt
def delete():

    # checks to see if the todo matches the user that's in the session
    todo = Todo.query.filter_by(
        user_id=current_user.id, id=request.form["delete"]
    ).first()

    if todo:
        db.session.delete(todo)
        db.session.commit()

    return redirect(url_for("landing.index"))
