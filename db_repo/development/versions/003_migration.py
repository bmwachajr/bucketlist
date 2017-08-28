from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
items = Table('items', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('description', String(length=120)),
    Column('date_created', DateTime, default=ColumnDefault(datetime.datetime(2017, 8, 3, 7, 20, 17, 843575))),
    Column('date_modified', DateTime, onupdate=ColumnDefault(datetime.datetime(2017, 8, 3, 7, 20, 17, 843610))),
    Column('bucketlist_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['items'].columns['description'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['items'].columns['description'].drop()
