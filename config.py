import os
class Config(object):
    DEBUG = False

class DevelopmentConfig(Config):
    SECRET_KEY = 'This is supposedly secret'

    # The following keys are from a test account I created. Please
    # replace them with your personal site keys before deploying on the
    # actual website, or else they won't work.
    RECAPTCHA_PUBLIC_KEY = '6LfqIxMTAAAAAFBX7k0jfutFr1gRFkD8lF7JYbuC'
    RECAPTCHA_PRIVATE_KEY = '6LfqIxMTAAAAAG6kDJu0xiy4uTgLjggbnFd3fFRG'

    if os.environ.get('OPENSHIFT_APP_NAME') is not None: # OpenShift setup
        print 'Detected OpenShift app. Loading parameters...'
        MONGODB_DB = os.environ.get('OPENSHIFT_APP_NAME')
        MONGODB_HOST = os.environ.get('OPENSHIFT_MONGODB_DB_HOST')
        MONGODB_PORT = int(os.environ.get('OPENSHIFT_MONGODB_DB_PORT', 0))
        MONGODB_USERNAME = os.environ.get('OPENSHIFT_MONGODB_DB_USERNAME')
        MONGODB_PASSWORD = os.environ.get('OPENSHIFT_MONGODB_DB_PASSWORD')
        
        DEBUG = False
    else:
        DEBUG = True
        MONGODB_SETTINGS = {'db': 'compassion'}
