import os


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.getenv("SECRET_KEY", "rand0102323")


class DevConfig(BaseConfig):
    # telling sqlalchemy where our database lives
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or "sqlite:///dev.db"
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_ECHO = True
    # SECRET_KEY = os.getenv('SECRET_KEY')


class TestConfig(BaseConfig):
    # same as above except renamed as the test database
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    WTF_CSRF_ENABLED = False
    TESTING = True
    # run jobs instantly, without needing to spin up a worker in testing


class ProdConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY")


configurations = {"dev": DevConfig, "test": TestConfig, "prod": ProdConfig}
