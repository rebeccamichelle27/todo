from flask import Blueprint, render_template

landing_bp = Blueprint("landing", __name__)


@landing_bp.route("/", methods=["GET", "POST"])
def index():
    return "Hello World!"


# decorate with login_required

# username = None
# todos = None

# form = LoginForm()

# if current_user.is_authenticated:
#     form = ToDoForm()

#     username = current_user.name
#     user = User.query.filter_by(name=username).first()
#     todos = user.todos

# if request.method == "POST":

#     if form.validate_on_submit():
#         user.todos.append(Todo(name=form.todo.data))
#         db.session.commit()
#         return redirect(url_for("index"))

# return render_template("index.html", username=username, todos=todos, form=form)

