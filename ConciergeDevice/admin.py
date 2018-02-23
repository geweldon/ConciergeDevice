from django.contrib import admin
from .models import DeviceTypes,  Devices

admin.register(DeviceTypes, Devices)(admin.ModelAdmin)
