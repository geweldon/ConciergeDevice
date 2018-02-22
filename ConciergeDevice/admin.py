from django.contrib import admin
from models import DeviceTypes, CommandModel, Devices

admin.register(DeviceTypes, CommandModel, Devices)
