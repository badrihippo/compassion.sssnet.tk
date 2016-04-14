from flask import Flask
from flask_mongoengine import MongoEngine

app = Flask(__name__)
try:
    app.config.from_pyfile('../instance/config.py')
except:
    print 'Using development config...'
    app.config.from_object('config.DevelopmentConfig')

db = MongoEngine(app)
