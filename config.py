class Config(object):
    DEBUG = False

class DevelopmentConfig(Config):
    SECRET_KEY = 'This is supposedly secret'
    DEBUG = True
    MONGODB_SETTINGS = {'db': 'compassion'}

    # The following keys are from a test account I created. Please
    # replace them with your personal site keys before deploying on the
    # actual website, or else they won't work.
    RECAPTCHA_PUBLIC_KEY = '6LfqIxMTAAAAAFBX7k0jfutFr1gRFkD8lF7JYbuC'
    RECAPTCHA_PRIVATE_KEY = '6LfqIxMTAAAAAG6kDJu0xiy4uTgLjggbnFd3fFRG'
