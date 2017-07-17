import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLACLHEMY_DATABASE_URI = 'sqlitte:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repo')
