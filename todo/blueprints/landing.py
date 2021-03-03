from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from todo.forms import ToDoForm
from todo.models import User, Todo
from todo.extensions import db

landing_bp = Blueprint("landing", __name__)


@landing_bp.route("/", methods=["GET", "POST"])
def index():

    form = ToDoForm()

    if form.validate_on_submit():
        current_user.todos.append(Todo(name=form.todo.data))
        db.session.commit()
        return redirect(url_for("landing.index"))

    return render_template("landing/index.html", form=form)

