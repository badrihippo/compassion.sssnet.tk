from django.contrib import admin

from media.models import Picture, Country, StateProvince, Address

for model in (Picture, Country, StateProvince, Address):
    admin.site.register(model)