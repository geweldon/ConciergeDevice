import requests

def commandSelector(commands, cmd):
    for command in commands:
        if cmd == command.command_name:
            return command
    return None

def stateUpdater(response, device, *args, **kwargs):
    res = response.json()["success"]
    status = any(res.values())

    if status != device.status:
        device.status = status
        device.save(update_fields=['status'])

    pass

def phillipsHueHandler(device_object, cmd, arguments, **kwargs):
    device = device_object
    commands = device.device_type.commands
    command = commandSelector(commands=commands, cmd=cmd)
    ip = device.ip
    name = device.name

    r = command.command_string.format(ip, name)
    message = command.command_message
    res = requests.put(r, data=message)

    stateUpdater(res, device)

    return res
