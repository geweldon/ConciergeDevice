from graphene_django import DjangoObjectType
from .models import Devices, DeviceTypes, CommandModel
import graphene
import requests
from . import device_handlers


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
    all_devices = graphene.List(Device)
    device = graphene.Field(Device, id=graphene.Int())
    device_commands = graphene.List(Command, id=graphene.Int())

    def resolve_all_devices(self, info, **kwargs):
        return Devices.objects.select_related('device_type').all()

    def resolve_device(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Devices.objects.select_related('device_type').get(pk=id)

        return None

    def resolve_device_commands(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            device = Devices.objects.select_related('device_type').get(pk=id)
            return device.device_type.commands

        return None


class SendCommand(graphene.Mutation):
    class Arguments:
        device_id = graphene.Int(required=True)
        command = graphene.String(required=True)
        arguments = graphene.List(graphene.String())

    ok = graphene.Boolean()
    response = graphene.String()

    def mutate(self, info, device_id, command, arguments):
        id = device_id
        command = command
        arguments = arguments

        device = Devices.objects.select_related('device_type').get(pk=id)
        handler = getattr(device_handlers, device.device_type.device_handler)

        request = handler(device, command, arguments)
        ok = request.status_code == requests.codes.ok
        response = request.text
        handler(device, command, arguments)

        return SendCommand(ok=ok, response=response)


class Mutation(graphene.ObjectType):
    send_command = SendCommand.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
