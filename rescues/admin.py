from django.contrib import admin

from rescues.models import Rescuer, RescueGroup, Species

for model in [Rescuer, RescueGroup, Species]:
    admin.site.register(model)