import os

basedir = os.path.abspath(os.path.dirname(__file__))

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
database = os.getenv("POSTGRES_DB")
DATABASE_URL = f"postgres://{user}:{password}@db:5432/{database}"


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "ahdndbduej174746490@$##%#$##%")
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    # Test and production database should be close as possible
    # But the sake of this task, I'm gonna use sqlite for test databaseß
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir,'test.db')}"

    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


config_by_name = dict(dev=DevelopmentConfig, test=TestingConfig, prod=ProductionConfig)

key = Config.SECRET_KEY
