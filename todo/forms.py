from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField
from wtforms.validators import Length, required, EqualTo
from werkzeug.security import check_password_hash
from todo.models import User

# look at user validation, how it was done in my other todo app vs yumroad vs miguel
class LoginForm(FlaskForm):
    username = StringField("Username:", validators=[required()])
    password = PasswordField("Password:", validators=[required()])

    def validate_username(self, username):
        user = User.query.filter_by(name=username.data).first()
        if not user or not check_password_hash(user.password, self.password.data):
            self.username.errors.append("Invalid email or password.")

    # add validation here


class RegisterForm(FlaskForm):
    username = StringField("Username:", validators=[required()])
    password = PasswordField(
        "Password:",
        validators=[
            required(),
            Length(min=4),
            EqualTo("confirm", message="Passwords must match"),
        ],
    )
    confirm = PasswordField("Confirm Password:")

    def validate_username(self, username):
        user = User.query.filter_by(name=username.data).first()
        if user:
            self.username.errors.append("That email already has an account.")


class ToDoForm(FlaskForm):
    todo = StringField("To do:", validators=[required(), Length(min=4, max=60)])
