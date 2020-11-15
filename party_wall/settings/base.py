import os
import datetime


# TODO: I should raise ImproperlyConfigured exception if something is not set
class Config:
    # APPLICATION SETTINGS
    DEBUG = os.getenv("DEBUG")
    APP_NAME = os.getenv("APP_NAME", "party-wall")
    PORT = os.getenv("PORT", "8000")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")

    # AUTHENTICATION SETTINGS
    SECRET_KEY = os.getenv("SECRET_KEY")
    REMEMBER_COOKIE_DURATION = datetime.timedelta(days=7)
    REMEMBER_COOKIE_REFRESH_EACH_REQUEST = False
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = None
    REMEMBER_COOKIE_DOMAIN = None

    # DATABASE SETTINGS
    DATABASE_DIALECT = os.getenv("DATABASE_DIALECT")
    DATABASE_HOST = os.getenv("DATABASE_HOST")
    DATABASE_PORT = os.getenv("DATABASE_PORT")
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    DATABASE_USER = os.getenv("DATABASE_USER")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
    SQLALCHEMY_DATABASE_URI = f"{DATABASE_DIALECT}://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
