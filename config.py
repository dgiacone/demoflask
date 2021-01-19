import os
class Config(object):
    SECRET_KEY='Este_es_mi Token_456789'

class DevelopmentConfig(Config):
    DEBUG=True
