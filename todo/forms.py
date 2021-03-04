from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField
from wtforms.validators import Length, required, EqualTo, email
from werkzeug.security import check_password_hash
from todo.models import User

# look at user validation, how it was done in my other todo app vs yumroad vs miguel
class LoginForm(FlaskForm):
    email = StringField("Email:", validators=[required()])
    password = PasswordField("Password:", validators=[required()])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user or not check_password_hash(user.password, self.password.data):
            self.email.errors.append("Invalid email or password.")


class RegisterForm(FlaskForm):
    email = StringField("Email:", validators=[email(), required(), Length(min=4)])
    password = PasswordField(
        "Password:",
        validators=[
            required(),
            Length(min=4),
            EqualTo("confirm", message="Passwords must match"),
        ],
    )
    confirm = PasswordField("Confirm Password:")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            self.email.errors.append("That email already has an account.")


class ToDoForm(FlaskForm):
    todo = StringField("New to do:", validators=[required(), Length(min=4, max=60)])
