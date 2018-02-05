from graphene_django import DjangoObjectType
from models import DeviceModel
import graphene


class Device(DjangoObjectType):
    class Meta:
        model = DeviceModel


class Query(graphene.ObjectType):
    devices = graphene.list(Device)

    def resolve_devices(self, info):
        return DeviceModel.objects.all()

schema = graphene.Schema(query=Query)
