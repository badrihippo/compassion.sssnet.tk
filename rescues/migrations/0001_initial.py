# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('media', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('gender', models.CharField(max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female'), (b'?', b'Unknown')])),
                ('rescue_time', models.DateTimeField(null=True, blank=True)),
                ('birthday', models.DateField(null=True, blank=True)),
                ('description', models.TextField(blank=True)),
                ('is_adopted', models.BooleanField(default=False)),
                ('photos', models.ManyToManyField(to='media.Picture')),
            ],
        ),
        migrations.CreateModel(
            name='RescueGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('phone', models.CharField(max_length=12)),
                ('about_us', models.TextField()),
                ('address', models.OneToOneField(to='media.Address')),
                ('admin', models.ForeignKey(related_name='my_groups', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rescuer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gender', models.CharField(max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female'), (b'?', b'Unknown')])),
                ('avatar', models.ImageField(upload_to=b'img/profiles')),
                ('phone_country', models.CharField(max_length=4)),
                ('phone', models.CharField(max_length=12)),
                ('about_me', models.TextField()),
                ('address', models.OneToOneField(to='media.Address')),
                ('rescue_group', models.ForeignKey(related_name='people', blank=True, to='rescues.RescueGroup')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('scientific_name', models.CharField(max_length=128, blank=True)),
                ('about', models.TextField(blank=True)),
                ('icon', models.ForeignKey(blank=True, to='media.Picture', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='pet',
            name='species',
            field=models.ForeignKey(to='rescues.Species'),
        ),
    ]
