from django.contrib import admin
from .models import Temperature, pH, DistilledOxygen, Pressure

# Register your models here.

admin.site.register(Temperature)
admin.site.register(pH)
admin.site.register(DistilledOxygen)
admin.site.register(Pressure)
