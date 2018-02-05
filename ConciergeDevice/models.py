from djongo import models


class DeviceType(models.Model):
    device_type = models.CharField(max_length=100)
    commands = models.ArrayModelField(model_container='Command')


class Command(models.Model):
    command_name = models.CharField(max_length=100)
    command_string = models.TextField()

    class Meta:
        abstract = True


class DeviceModel(models.Model):
    device_name = models.CharField(max_length=100)
    mac_address = models.CharField(max_length=100)
    device_IP = models.CharField(max_length=100)
    device_type = models.ForeignKey('DeviceType', on_delete=models.CASCADE)
    device_status = models.CharField(max_length=100)
