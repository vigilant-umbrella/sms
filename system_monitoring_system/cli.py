import core
from exceptions import ArgumentError
import getpass
import json
import keyring
import os
import report


def summary():
    """
    Display a summary of System usage data
    """
    g = core.Get()

    text = 'OS: {} \t Uptime: {}'.format(g.os(), g.uptime())
    print(text)

    # CPU data
    text = '\nCPU:-'
    print(text)
    cpu_dict = g.cpu()
    text = 'Load Average: {} {} {} \t User: {} % \t System: {} %'.format(
        cpu_dict['load_avg'][0], cpu_dict['load_avg'][1], cpu_dict['load_avg'][2], cpu_dict['user'], cpu_dict['system'])
    print(text)
    text = 'Idle: {} % \t I/O Wait: {} % \t Cores: {}'.format(
        cpu_dict['idle'], cpu_dict['iowait'], cpu_dict['num_cores'])
    print(text)

    # Memory data
    text = '\nMemory:-'
    print(text)
    memory_dict = g.memory()
    text = 'Total: {:,} Bytes \t Used: Used: {:,} Bytes \t Free: {:,} Bytes'.format(
        memory_dict['total'], memory_dict['used_incl'], memory_dict['free'])
    print(text)

    # Network data
    text = '\nNetwork:-'
    print(text)
    networks = g.network()
    for network_dict in networks:
        text = 'Interface: {} \t IP: {}'.format(
            network_dict['interface'], network_dict['ip'])
        print(text)

    # Storage data
    text = '\nStorage:-'
    print(text)
    storages = g.storage()
    for storage_dict in storages:
        text = 'Device: {} \t Mounted: {} \t Total: {:,} Bytes'.format(
            storage_dict['device'], storage_dict['mountpoint'], storage_dict['total'])
        print(text)
        text = 'Used: {:,} Bytes ({}%) \t Free: {:,} Bytes'.format(
            storage_dict['used'], storage_dict['percent'], storage_dict['free'])
        print(text)

    # Swap data
    text = '\nSwap:-'
    print(text)
    swap_dict = g.swap()
    text = 'Total: {:,} Bytes \t Used: {:,} Bytes ({}%) \t Free: {:,} Bytes'.format(
        swap_dict['total'], swap_dict['used'], swap_dict['percent'], swap_dict['free'])
    print(text)
    text = 'Swapped in: {:,} Bytes \t Swapped out: {:,} Bytes'.format(
        swap_dict['sin'], swap_dict['sout'])
    print(text)

    # Users data
    text = '\nUsers:-'
    print(text)
    users = g.users()
    for user_dict in users:
        text = 'Name: {} \t Session started: {} \t Host: {}'.format(
            user_dict['name'], user_dict['sess_started'], user_dict['host'])
        print(text)


def cpu():
    """
    Display detailed CPU usage data
    """
    pass


def memory():
    """
    Display detailed Memory usage data
    """
    pass


def process():
    """
    Display detailed Process usage data
    """
    pass


def storage():
    """
    Display detailed Storage usage data
    """
    pass


def network():
    """
    Display detailed Network usage data
    """
    pass


def misc():
    """
    Display Miscellaneous usage data
    """
    pass


def show_limit():
    settings_file = open(os.path.join(
        os.path.expanduser('~'), '.sms/settings.json'))
    settings = json.load(settings_file)
    settings_file.close()

    for resource, value in settings['limit'].items():
        print('{} - {}'.format(resource, value))


def update_limit(resource, limit):
    if resource not in ['cpu', 'memory', 'storage', 'swap']:
        msg = """
Invalid resource name entered.

Valid resource names are:
 - cpu
 - memory
 - storage
 - swap
"""
        raise ArgumentError(msg)

    if limit >= 100 or limit <= 0:
        msg = """
Invalid limit entered.

Limit must be between 0 and 100.
"""
        raise ArgumentError(msg)

    file_path = os.path.join(os.path.expanduser('~'), '.sms/settings.json')
    settings_file = open(file_path)
    settings = json.load(settings_file)
    settings_file.close()

    settings['limit'][resource] = limit

    with open(file_path, 'w') as f:
        json.dump(settings, f)


def show_email():
    settings_file = open(os.path.join(
        os.path.expanduser('~'), '.sms/settings.json'))
    settings = json.load(settings_file)
    settings_file.close()

    for email, name in settings['email'].items():
        print('{} - {}'.format(name, email))


def update_email(action, *args):
    if action not in ['add', 'modify', 'remove']:
        msg = """
Invalid action entered.

Valid actions are:
 - add
 - modify
 - remove
"""
        raise ArgumentError(msg)

    if action == 'add':
        if len(args) != 2:
            raise ArgumentError
        add_email(*args)
    elif action == 'modify':
        if len(args) != 4:
            raise ArgumentError
        modify_email(*args)
    elif action == 'remove':
        if len(args) != 1:
            print(args)
            raise ArgumentError
        remove_email(*args)


def add_email(name, email):
    file_path = os.path.join(os.path.expanduser('~'), '.sms/settings.json')
    settings_file = open(file_path)
    settings = json.load(settings_file)
    settings_file.close()

    settings['email'][email] = name

    with open(file_path, 'w') as f:
        json.dump(settings, f)


def modify_email(old_name, old_email, new_name, new_email):
    file_path = os.path.join(os.path.expanduser('~'), '.sms/settings.json')
    settings_file = open(file_path)
    settings = json.load(settings_file)
    settings_file.close()

    if old_email not in settings['email']:
        msg = 'email provided does not exist.'
        raise ArgumentError(msg)

    del settings['email'][old_email]

    settings['email'][new_email] = new_name

    with open(file_path, 'w') as f:
        json.dump(settings, f)


def remove_email(email):
    file_path = os.path.join(os.path.expanduser('~'), '.sms/settings.json')
    settings_file = open(file_path)
    settings = json.load(settings_file)
    settings_file.close()

    if email not in settings['email']:
        msg = 'email provided does not exist.'
        raise ArgumentError(msg)

    del settings['email'][email]

    with open(file_path, 'w') as f:
        json.dump(settings, f)


def update_password():
    user_old_password = getpass.getpass(prompt='Old Password: ')
    old_password = keyring.get_password('sms_password', 'Administrator')
    if user_old_password != old_password:
        print('\nWrong Password entered')
        return

    new_password = getpass.getpass(prompt='New Password: ')
    conf_new_password = getpass.getpass(prompt='Confirm New Password: ')
    if new_password != conf_new_password:
        print('\nPassword Mismatch')
        return

    keyring.set_password('sms_password', 'Administrator', new_password)


def send_email(resource='Summary'):
    email = input('Google account email: ')
    password = getpass.getpass()
    report.send_email(email, password, resource)

    print('Mail Sent')


if __name__ == '__main__':
    exit()
