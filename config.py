import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bide.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'ykuyutkytkytkytk'


class DevelopementConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEVELOPMENT_DATABASE_URI') or \
                              'sqlite:///bide.db'


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI') or \
                              'postgresql://postgres:gfhjkbr1A@localhost:5432/flask'
