from django.db import models

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('?', 'Unknown')
    )

class Rescuer(models.Model):
    user = models.OneToOneField('auth.User')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    avatar = models.ImageField(upload_to='img/profiles')
    phone_country = models.CharField(max_length=4) # Country code
    phone = models.CharField(max_length=12)
    address = models.OneToOneField('media.Address')
    about_me = models.TextField()
    rescue_group = models.ForeignKey('rescues.RescueGroup', 
        related_name='people',
        blank=True)
    
class RescueGroup(models.Model):
    name = models.CharField(max_length=32)
    address = models.OneToOneField('media.Address')
    phone = models.CharField(max_length=12)
    admin = models.ForeignKey('auth.User',
        related_name='my_groups')
    about_us = models.TextField()
    
class Pet(models.Model):
    name = models.CharField(max_length=32)
    species = models.ForeignKey('rescues.Species')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    rescue_time = models.DateTimeField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    is_adopted = models.BooleanField(default=False)
    photos = models.ManyToManyField('media.Picture')

class Species(models.Model):
    name = models.CharField(max_length=128)
    scientific_name = models.CharField(max_length=128, blank=True)
    icon = models.ForeignKey('media.Picture', blank=True, null=True)
    about = models.TextField(blank=True)
    