import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """ Default Cinfiguration """

    DEBUG = True
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(basedir, '/databases/app.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repo')


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

    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(basedir, 'databases/app.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repo/production')


environment_configuration = {
    'development': Development,
    'testing': Testing,
    'Production': Production
}
