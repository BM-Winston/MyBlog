from flask import config
import os

class Config:

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY='SECRET_KEY'
    
    # SECRET_KEY = os.environ.get('SECRET_KEY')

    

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL","")
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI =SQLALCHEMY_DATABASE_URI.replace("postgres://","postgresql://",)

    

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:Access@localhost/blogs'
    DEBUG = True

class TestConfig(Config):

    pass

config_options = {
    'development': DevConfig,
    'production': ProdConfig,
    'test': TestConfig
}
