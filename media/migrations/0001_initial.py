# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address_line1', models.CharField(max_length=45, verbose_name=b'Address line 1')),
                ('address_line2', models.CharField(max_length=45, verbose_name=b'Address line 2', blank=True)),
                ('postal_code', models.CharField(max_length=10, verbose_name=b'Postal Code')),
                ('city', models.CharField(max_length=50)),
                ('state_province', models.CharField(max_length=40, verbose_name=b'State/Province', blank=True)),
            ],
            options={
                'verbose_name_plural': 'Addresses',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('iso_code', models.CharField(max_length=2, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'ordering': ['name', 'iso_code'],
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('caption', models.CharField(max_length=300, blank=True)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(null=True, upload_to=b'img/photos', blank=True)),
                ('credit', models.TextField(blank=True)),
                ('url', models.URLField(blank=True)),
                ('owner', models.ForeignKey(related_name='my_pics', to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StateProvince',
            fields=[
                ('iso_code', models.CharField(max_length=3, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=55)),
                ('country', models.ForeignKey(to='media.Country')),
            ],
            options={
                'verbose_name': 'State or province',
            },
        ),
        migrations.AddField(
            model_name='address',
            name='country',
            field=models.ForeignKey(to='media.Country'),
        ),
        migrations.AlterUniqueTogether(
            name='address',
            unique_together=set([('address_line1', 'address_line2', 'postal_code', 'city', 'state_province', 'country')]),
        ),
    ]
