from flask_login import UserMixin
from flask_mongoengine.wtf import model_form
import datetime
from .app import db

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('?', 'Unknown')
    )
class BinaryFile(db.Document):
    filename = db.StringField(max_length=255, required=True)
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    payload = db.FileField(required=True)
    meta = {'allow_inheritance': True}

class ImageFile(BinaryFile):
    payload = db.ImageField(size=(800, 600, True), thumbnail_size=(100, 100, True), required=True)

class ContactPhone(db.EmbeddedDocument):
    title = db.StringField(max_length=32)
    country_code = db.StringField(max_length=4)
    number = db.StringField(max_length=12)
    extra_info = db.StringField()

class ContactAddress(db.EmbeddedDocument):
    title = db.StringField(max_length=32) # Address title
    name = db.StringField(max_length=64)
    address = db.StringField()
    pin_code = db.StringField(max_length=8)
    country_code = db.StringField(max_length=2) #TODO: Specify choices
    extra_info = db.StringField()

class ContactEmail(db.EmbeddedDocument):
    email = db.EmailField()
    extra_info = db.StringField()

class ContactUnverifiedEmail(db.EmbeddedDocument):
    email = db.EmailField()
    verification_code = db.StringField()
    allowed_letters = 'abcdefghjkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ023456789'

class User(db.Document, UserMixin):
    first_name = db.StringField(max_length=32)
    last_name = db.StringField(max_length=32)
    username = db.StringField(max_length=32, unique=True)
    password = db.StringField(max_length=128, required=True)
    gender = db.StringField(max_length=1, choices=GENDER_CHOICES)
    avatar = db.ImageField(size=(128,128, True))
    emails = db.ListField(db.EmbeddedDocumentField(ContactEmail))
    phones = db.ListField(db.EmbeddedDocumentField(ContactPhone))
    addresses = db.ListField(db.EmbeddedDocumentField(ContactAddress))
    about_me = db.StringField()
    rescue_group = db.ReferenceField('RescueGroup')

    # Unverified
    unverified_emails = db.ListField(db.EmbeddedDocumentField(ContactUnverifiedEmail))

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)
    
class RescueGroup(db.Document):
    name = db.StringField(max_length=32)
    emails = db.ListField(db.EmbeddedDocumentField(ContactEmail))
    phones = db.ListField(db.EmbeddedDocumentField(ContactPhone))
    addresses = db.ListField(db.EmbeddedDocumentField(ContactAddress))
    admin = db.ListField(db.ReferenceField(User)) # Group administrator
    about_us = db.StringField()

class Species(db.Document):
    name = db.StringField(max_length=128, required=True)
    scientific_name = db.StringField(max_length=128)
    icon = db.ImageField(size=(32,32,True))
    about = db.StringField()

class Pet(db.Document):
    name = db.StringField(max_length=32)
    species = db.ReferenceField(Species, required=True)
    gender = db.StringField(max_length=1, choices=GENDER_CHOICES)
    rescue_time = db.DateTimeField()
    birthday = db.DateTimeField()
    description = db.StringField()
    is_adopted = db.BooleanField(default=False)
    photos = db.ListField(db.ReferenceField(ImageFile))
    rescuer = db.GenericReferenceField(choices=(User, RescueGroup))
