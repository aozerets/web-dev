import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'fj894h3h8ghi@#%$^'


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    SERVER_NAME = 'localhost:8082'
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
