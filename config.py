import os
basedir = os.path.abspath(os.path.dirname(__file__))

# The basic configuration class from which other config classes inherit from
class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this is octopos'
    # Database connection string
    # Please note that this should ideally be: SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    # Where DATABASE_URL can be added as a system property
    SQLALCHEMY_DATABASE_URI = 'mysql://generic:generic@130.211.185.22/octopos' 

# Production environment config
class ProductionConfig(Config):
    DEBUG = False


# Development envionment config
class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

# Testing environment config
class TestingConfig(Config):
    TESTING = True