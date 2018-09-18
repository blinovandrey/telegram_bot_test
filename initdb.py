from config import DATABASE

import sqlalchemy

from models import Base


def get_db_config():
    try:
        db_host = DATABASE['host']
        db_name = DATABASE['dbname']
        db_user = DATABASE['user']
        db_password = DATABASE['password']
        db_port = DATABASE['port']
    except KeyError as e:
        print "Can not get {} from config".format(e.args[0])
    else:
        return db_user, db_password, db_host, db_port, db_name


def create_engine(db_user, db_password, db_host, db_port, db_name):
    url = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_password, db_host, db_port, db_name)

    try:
        engine = sqlalchemy.create_engine(url, client_encoding='utf8', echo=True)
    except Exception as e:
        print e.message
    else:
        return engine


db_config = get_db_config()
engine = create_engine(*db_config)

Base.metadata.create_all(engine)
