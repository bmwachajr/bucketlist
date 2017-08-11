import os
basedir = os.path.abspath(os.path.dirname(__file__))


# Set environmental settings
environment = 'development'

# Environmental settings
class Config(object):
    """ Default Configuration """

    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(basedir, '/databases/app.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repo')
    SECRET_KEY = "WK,gf#8V:y]ZzROB*mKjtOtu!PU:Fi"


class Development(Config):
    """ Development Configuration """

    DEBUG = True
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = 'False'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(basedir, 'databases/development.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repo/development')


class Testing(Config):
    """ Testing Configuration """

    DEBUG = True
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = 'False'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(basedir, 'databases/testing.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repo/testing')


class Production(Config):
    """ Production Configuration """

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(basedir, 'databases/app.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repo/production')


environment_configuration = {
    'development': Development,
    'testing': Testing,
    'Production': Production
}
