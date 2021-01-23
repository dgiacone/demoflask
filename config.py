import os
class Config(object):
    SECRET_KEY='Este_es_mi Token_456789'

class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI='mysql://nodesql:nodesql_123456@192.168.0.106/node'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
