from djongo import models
from djongo.models import forms



class CommandModel(models.Model):
    command_name = models.CharField(max_length=100)
    command_string = models.TextField()
    command_message = models.CharField(max_length=100)

    class Meta:
        abstract = True


class CommandForm(forms.ModelForm):
    class Meta:
        model = CommandModel
        fields = ('command_name', 'command_string')


class DeviceTypes(models.Model):
    device_type = models.CharField(max_length=100)
    device_handler = models.CharField(max_length=100)
    commands = models.ArrayModelField(model_container=CommandModel,
                                        model_form_class=CommandForm)

    def __string__(self):
        return self.device_type


class DeviceTypeForm(forms.ModelForm):
    class Meta:
        model = DeviceTypes
        fields = ('device_type', 'commands')

class Devices(models.Model):
    name = models.CharField(max_length=100)
    mac_address = models.CharField(max_length=100)
    ip = models.CharField(max_length=100)
    device_type = models.ForeignKey(
        'DeviceTypes', related_name='devices', on_delete=models.CASCADE)
    status = models.CharField(max_length=100)

    def __string__(self):
        return self.name


class DeviceModelForm(forms.ModelForm):
    class META:
        model = Devices
        fields = (
            'device_name', 'mac_address', 'device_IP', 'device_type',
            'device_status'
        )
