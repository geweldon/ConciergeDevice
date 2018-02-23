from graphene_django import DjangoObjectType
from .models import Devices, DeviceTypes, CommandModel
import graphene


class Device(DjangoObjectType):
    class Meta:
        model = Devices


class DeviceType(DjangoObjectType):
    class Meta:
        model = DeviceTypes


class Command(DjangoObjectType):
    class Meta:
        model = CommandModel


class Query(graphene.ObjectType):
    devices = graphene.list(Device)
    device_commands = graphene.list(Command)

    def resolve_devices(self, info, **kwargs):
        return Devices.objects.select_related('device_type').all()

    def resolve_device_commands(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            device = Devices.objects.select_related('device_type').get(pk=id)
            return device.device_type.commands

        return None


schema = graphene.Schema(query=Query)
