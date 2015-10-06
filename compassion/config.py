class Config(object):
    DEBUG = False

class DevelopmentConfig(Config):
    SECRET_KEY = 'This is supposedly secret'
    DEBUG = True
    MONGODB_SETTINGS = {'db': 'compassion'}
