from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy import MetaData
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
login_manager = LoginManager()
csrf = CSRFProtect()
migrate = Migrate()
