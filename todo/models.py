from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from todo.extensions import db
from sqlalchemy.orm import validates


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    todos = db.relationship("Todo")

    @validates("username")
    def validate_username(self, key, username):
        if len(username.strip()) <= 3:
            raise ValueError("needs to have a username")
        return username

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method="sha256")

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<(User(id={self.id}, name={repr(self.username)}, todos={repr(self.todos)})>"


class Todo(db.Model):

    __tablename__ = "todos"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return f"<(Todo(id={self.id}, name={repr(self.name)}, user_id={self.user_id})>"

    @validates("name")
    def validate_name(self, key, name):
        if len(name.strip()) <= 3:
            raise ValueError("needs to have a name")
        return name