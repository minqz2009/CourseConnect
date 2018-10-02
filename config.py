import os

class Config(object):
    DEBUG=True
    SECRET_KEY='abc123'
    # SQLALCHEMY_DATABASE_URI='postgresql://@localhost/1531'
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'dan.db')
    SQLALCHEMY_TRACK_MODIFICATIONS=False
